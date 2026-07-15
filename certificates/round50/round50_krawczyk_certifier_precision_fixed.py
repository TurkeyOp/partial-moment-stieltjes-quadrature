#!/usr/bin/env python3
"""Round 50 interval Krawczyk certifier for six upper-half rules.

The certificate is for the explicitly reconstructed square system:
  * k moment equations;
  * d+1 signed equal-error equations, d = 2n-k;
  * d-1 internal stationarity equations.

A successful verdict requires both componentwise Krawczyk inclusion and
||I-YJ(X)||_infinity < 1, plus ordered positive parameter margins.
"""
from __future__ import annotations
import argparse, csv, json, hashlib
from pathlib import Path
import mpmath as mp
from flint import arb, ctx

PROBLEMS = [(2,3),(3,4),(3,5),(4,5),(4,6),(4,7)]
# Endpoint values are constructed after mp.mp.dps is set; avoid import-time rounding.
BLEFT_TEXT = '0.08'; BRIGHT_TEXT = '0.12'


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1<<20), b''): h.update(chunk)
    return h.hexdigest()


def load_center(nodes_csv: Path, alt_csv: Path, n: int, k: int):
    with nodes_csv.open(newline='', encoding='utf-8') as f:
        nr=[r for r in csv.DictReader(f) if int(r['node_pairs_n'])==n and int(r['matched_moments_k'])==k]
    with alt_csv.open(newline='', encoding='utf-8') as f:
        ar=[r for r in csv.DictReader(f) if int(r['node_pairs_n'])==n and int(r['matched_moments_k'])==k]
    nr.sort(key=lambda r:int(r['node_index'])); ar.sort(key=lambda r:int(r['extremum_index']))
    if len(nr)!=n: raise ValueError(f'Expected {n} node rows for {(n,k)}, got {len(nr)}')
    d=2*n-k
    if len(ar)!=d+1: raise ValueError(f'Expected {d+1} extrema rows for {(n,k)}, got {len(ar)}')
    y=[mp.mpf(r['squared_node_y']) for r in nr]
    w=[mp.mpf(r['pair_weight']) for r in nr]
    bs=[mp.mpf(r['b']) for r in ar]
    signs=[1 if mp.mpf(r['relative_error'])>0 else -1 for r in ar]
    if any(signs[i+1]!=-signs[i] for i in range(len(signs)-1)):
        raise ValueError(f'Non-alternating signs in input for {(n,k)}: {signs}')
    E=max(abs(mp.mpf(r['relative_error'])) for r in ar)
    return mp.matrix(y+w+bs[1:-1]+[E]), signs


def f0(b): return 2*mp.atan(1/b)/b

def f1(b): return -2/(b*(1+b*b))-2*mp.atan(1/b)/(b*b)

def f2(b):
    A=mp.atan(1/b)
    return (2*(1+3*b*b)/(b*b*(1+b*b)**2)
            +2/(b*b*(1+b*b))+4*A/(b**3))


def eval_mp(z, n, k, signs):
    d=2*n-k; q=d-1; m=d+1; N=4*n-k
    y=[z[i] for i in range(n)]; w=[z[n+i] for i in range(n)]
    bs=[mp.mpf(BLEFT_TEXT)]+[z[2*n+i] for i in range(q)]+[mp.mpf(BRIGHT_TEXT)]
    E=z[N-1]
    f=mp.matrix(N,1); J=mp.matrix(N,N)
    row=0
    for ell in range(k):
        f[row]=sum(w[j]*y[j]**ell for j in range(n))-mp.mpf(1)/(2*ell+1)
        for j in range(n):
            J[row,j]=0 if ell==0 else w[j]*ell*y[j]**(ell-1)
            J[row,n+j]=y[j]**ell
        row+=1
    caches=[]
    for b in bs:
        F=f0(b); Fb=f1(b); Fbb=f2(b)
        D=[b*b+y[j] for j in range(n)]
        r=2*sum(w[j]/D[j] for j in range(n))
        rb=-4*b*sum(w[j]/D[j]**2 for j in range(n))
        rbb=-4*sum(w[j]/D[j]**2 for j in range(n))+16*b*b*sum(w[j]/D[j]**3 for j in range(n))
        eps=r/F-1
        epsb=(rb*F-r*Fb)/(F**2)
        epsbb=rbb/F-r*Fbb/(F**2)-2*rb*Fb/(F**2)+2*r*Fb*Fb/(F**3)
        dey=[-2*w[j]/(F*D[j]**2) for j in range(n)]
        dew=[2/(F*D[j]) for j in range(n)]
        dby=[]; dbw=[]
        for j in range(n):
            dry=-2*w[j]/D[j]**2; drby=8*b*w[j]/D[j]**3
            drw=2/D[j]; drbw=-4*b/D[j]**2
            dby.append((drby*F-dry*Fb)/(F**2))
            dbw.append((drbw*F-drw*Fb)/(F**2))
        caches.append((eps,epsb,epsbb,dey,dew,dby,dbw))
    for i in range(m):
        eps,epsb,epsbb,dey,dew,dby,dbw=caches[i]
        f[row]=eps-signs[i]*E
        for j in range(n): J[row,j]=dey[j]; J[row,n+j]=dew[j]
        if 0<i<m-1: J[row,2*n+i-1]=epsb
        J[row,N-1]=-signs[i]
        row+=1
    for i in range(1,m-1):
        eps,epsb,epsbb,dey,dew,dby,dbw=caches[i]
        f[row]=epsb
        for j in range(n): J[row,j]=dby[j]; J[row,n+j]=dbw[j]
        J[row,2*n+i-1]=epsbb
        row+=1
    assert row==N
    return f,J


def refine(z, n, k, signs, tol):
    history=[]
    for it in range(20):
        f,J=eval_mp(z,n,k,signs)
        res=max(abs(v) for v in f); history.append(mp.nstr(res,12))
        if res<tol: return z,f,J,history
        z=z+mp.lu_solve(J,-f)
    f,J=eval_mp(z,n,k,signs)
    return z,f,J,history


def A(x): return arb(mp.nstr(x, mp.mp.dps-20))

def ball(center, radius): return arb(mp.nstr(center, mp.mp.dps-20), mp.nstr(radius, 30))

def arb_f0(b): return 2*(1/b).atan()/b

def arb_f1(b): return -2/(b*(1+b*b))-2*(1/b).atan()/(b*b)

def arb_f2(b):
    At=(1/b).atan()
    return 2*(1+3*b*b)/(b*b*(1+b*b)**2)+2/(b*b*(1+b*b))+4*At/(b**3)


def eval_arb(X, n, k, signs):
    d=2*n-k; q=d-1; m=d+1; N=4*n-k
    y=X[:n]; w=X[n:2*n]
    bs=[arb('0.08')]+X[2*n:2*n+q]+[arb('0.12')]
    E=X[N-1]
    fv=[arb(0) for _ in range(N)]; J=[[arb(0) for _ in range(N)] for __ in range(N)]
    row=0
    for ell in range(k):
        fv[row]=sum((w[j]*y[j]**ell for j in range(n)), arb(0))-arb(1)/(2*ell+1)
        for j in range(n):
            J[row][j]=arb(0) if ell==0 else w[j]*ell*y[j]**(ell-1)
            J[row][n+j]=y[j]**ell
        row+=1
    caches=[]
    for b in bs:
        F=arb_f0(b); Fb=arb_f1(b); Fbb=arb_f2(b)
        D=[b*b+y[j] for j in range(n)]
        r=2*sum((w[j]/D[j] for j in range(n)), arb(0))
        rb=-4*b*sum((w[j]/D[j]**2 for j in range(n)), arb(0))
        rbb=-4*sum((w[j]/D[j]**2 for j in range(n)), arb(0))+16*b*b*sum((w[j]/D[j]**3 for j in range(n)), arb(0))
        eps=r/F-1
        epsb=(rb*F-r*Fb)/(F**2)
        epsbb=rbb/F-r*Fbb/(F**2)-2*rb*Fb/(F**2)+2*r*Fb*Fb/(F**3)
        dey=[-2*w[j]/(F*D[j]**2) for j in range(n)]
        dew=[2/(F*D[j]) for j in range(n)]
        dby=[]; dbw=[]
        for j in range(n):
            dry=-2*w[j]/D[j]**2; drby=8*b*w[j]/D[j]**3
            drw=2/D[j]; drbw=-4*b/D[j]**2
            dby.append((drby*F-dry*Fb)/(F**2))
            dbw.append((drbw*F-drw*Fb)/(F**2))
        caches.append((eps,epsb,epsbb,dey,dew,dby,dbw))
    for i in range(m):
        eps,epsb,epsbb,dey,dew,dby,dbw=caches[i]
        fv[row]=eps-signs[i]*E
        for j in range(n): J[row][j]=dey[j]; J[row][n+j]=dew[j]
        if 0<i<m-1: J[row][2*n+i-1]=epsb
        J[row][N-1]=-signs[i]
        row+=1
    for i in range(1,m-1):
        eps,epsb,epsbb,dey,dew,dby,dbw=caches[i]
        fv[row]=epsb
        for j in range(n): J[row][j]=dby[j]; J[row][n+j]=dbw[j]
        J[row][2*n+i-1]=epsbb
        row+=1
    return fv,J


def abs_upper_float(x): return float(x.abs_upper())

def certify(z, Jmp, n, k, signs, exponent):
    N=4*n-k; radius=mp.power(10,-exponent)
    X=[ball(z[i],radius) for i in range(N)]
    zA=[A(z[i]) for i in range(N)]
    fpoint,_=eval_arb(zA,n,k,signs)
    _,JX=eval_arb(X,n,k,signs)
    Ymp=Jmp**-1
    Y=[[A(Ymp[i,j]) for j in range(N)] for i in range(N)]
    # B = I - Y J(X)
    B=[[arb(0) for _ in range(N)] for __ in range(N)]
    for i in range(N):
        for j in range(N):
            val=sum((Y[i][p]*JX[p][j] for p in range(N)), arb(0))
            B[i][j]=(arb(1) if i==j else arb(0))-val
    correction=[]; K=[]
    zero_balls=[arb(0, mp.nstr(radius,30)) for _ in range(N)]
    for i in range(N):
        c=zA[i]-sum((Y[i][p]*fpoint[p] for p in range(N)),arb(0))
        correction.append(c)
        kval=c+sum((B[i][j]*zero_balls[j] for j in range(N)),arb(0))
        K.append(kval)
    inclusion=[]; margins=[]
    for i in range(N):
        lm=K[i].lower()-X[i].lower(); um=X[i].upper()-K[i].upper()
        inclusion.append(bool(lm>0 and um>0)); margins.append(min(float(lm),float(um)))
    qnorm=max(sum(abs_upper_float(B[i][j]) for j in range(N)) for i in range(N))
    # domain margins from X
    y=X[:n]; w=X[n:2*n]; q=2*n-k-1; bs=X[2*n:2*n+q]; E=X[-1]
    order=[float(y[0].lower())]
    order += [float(y[j+1].lower()-y[j].upper()) for j in range(n-1)]
    order += [float(arb(1)-y[-1].upper())]
    positivity=[float(v.lower()) for v in w]
    bmargin=[]
    if q:
        bmargin.append(float(bs[0].lower()-arb('0.08')))
        bmargin += [float(bs[j+1].lower()-bs[j].upper()) for j in range(q-1)]
        bmargin.append(float(arb('0.12')-bs[-1].upper()))
    e_margin=float(E.lower())
    residuals,_=eval_arb(X,n,k,signs)
    residual_zero=[bool(r.lower()<=0 and r.upper()>=0) for r in residuals]
    success=(all(inclusion) and qnorm<1 and min(order)>0 and min(positivity)>0
             and (not bmargin or min(bmargin)>0) and e_margin>0 and all(residual_zero))
    return {
      'success':success,'radius_exponent':exponent,'radius':mp.nstr(radius,8),
      'q_norm_upper':qnorm,'minimum_inclusion_margin':min(margins),
      'all_components_included':all(inclusion),'all_residual_intervals_contain_zero':all(residual_zero),
      'minimum_y_ordering_margin':min(order),'minimum_weight_lower_bound':min(positivity),
      'minimum_b_ordering_margin':min(bmargin) if bmargin else None,'E_lower_bound':e_margin,
      'X':X,'K':K,'residuals':residuals,'B':B,'Ymp':Ymp
    }


def names(n,k):
    q=2*n-k-1
    return [f'y_{i+1}' for i in range(n)]+[f'w_{i+1}' for i in range(n)]+[f'b_{i+1}' for i in range(q)]+['E']


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--nodes-csv',type=Path,required=True); ap.add_argument('--alternation-csv',type=Path,required=True)
    ap.add_argument('--output-dir',type=Path,required=True); ap.add_argument('--mp-dps',type=int,default=180); ap.add_argument('--arb-dps',type=int,default=180)
    args=ap.parse_args(); args.output_dir.mkdir(parents=True,exist_ok=True)
    mp.mp.dps=args.mp_dps; ctx.dps=args.arb_dps
    all_summary=[]; all_boxes=[]; all_res=[]; detailed={}
    for n,k in PROBLEMS:
        z0,signs=load_center(args.nodes_csv,args.alternation_csv,n,k)
        z,f,J,hist=refine(z0,n,k,signs,mp.mpf('1e-140'))
        point_res=max(abs(v) for v in f); cond=mp.cond(J)
        cert=None; attempts=[]
        for exp in range(12,61):
            c=certify(z,J,n,k,signs,exp)
            attempts.append({kk:c[kk] for kk in ['radius_exponent','success','q_norm_upper','minimum_inclusion_margin']})
            if c['success']:
                cert=c; break
        if cert is None: cert=c
        verdict='CERTIFIED' if cert['success'] else 'FAILED'
        nm=names(n,k)
        for i,name in enumerate(nm):
            all_boxes.append({'n':n,'k':k,'variable':name,'center':mp.nstr(z[i],80),
              'radius':cert['radius'],'lower':str(cert['X'][i].lower()),'upper':str(cert['X'][i].upper()),
              'krawczyk_lower':str(cert['K'][i].lower()),'krawczyk_upper':str(cert['K'][i].upper())})
        for i,r in enumerate(cert['residuals']):
            kind='moment' if i<k else ('equal_error' if i<k+(2*n-k+1) else 'stationarity')
            all_res.append({'n':n,'k':k,'equation_index':i,'equation_type':kind,'lower':str(r.lower()),'upper':str(r.upper()),'contains_zero':bool(r.lower()<=0 and r.upper()>=0)})
        summary={'n':n,'k':k,'dimension_d':2*n-k,'unknowns':4*n-k,'equations':4*n-k,'internal_extrema':2*n-k-1,
          'sign_pattern':signs,'point_residual_max':mp.nstr(point_res,20),'jacobian_condition_estimate':mp.nstr(cond,12),
          'verdict':verdict,'radius':cert['radius'],'radius_exponent':cert['radius_exponent'],
          'krawczyk_q_norm_upper':cert['q_norm_upper'],'minimum_inclusion_margin':cert['minimum_inclusion_margin'],
          'minimum_y_ordering_margin':cert['minimum_y_ordering_margin'],'minimum_weight_lower_bound':cert['minimum_weight_lower_bound'],
          'minimum_b_ordering_margin':cert['minimum_b_ordering_margin'],'E_lower_bound':cert['E_lower_bound'],
          'all_residual_intervals_contain_zero':cert['all_residual_intervals_contain_zero']}
        all_summary.append(summary); detailed[f'n{n}_k{k}']={'summary':summary,'newton_history':hist,'attempts':attempts}
        print((n,k),verdict,'radius',cert['radius'],'qnorm',cert['q_norm_upper'])
    # CSV/JSON
    with (args.output_dir/'round50_certificate_summary.csv').open('w',newline='',encoding='utf-8') as f:
        cols=list(all_summary[0].keys()); w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(all_summary)
    with (args.output_dir/'round50_verified_boxes.csv').open('w',newline='',encoding='utf-8') as f:
        cols=list(all_boxes[0].keys()); w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(all_boxes)
    with (args.output_dir/'round50_residual_intervals.csv').open('w',newline='',encoding='utf-8') as f:
        cols=list(all_res[0].keys()); w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(all_res)
    result={'method':'Krawczyk with Arb interval Jacobian and numerical midpoint preconditioner',
      'precision':{'mp_dps':args.mp_dps,'arb_dps':args.arb_dps},'inputs':{'nodes_csv':str(args.nodes_csv),'nodes_sha256':sha256(args.nodes_csv),'alternation_csv':str(args.alternation_csv),'alternation_sha256':sha256(args.alternation_csv)},
      'all_six_certified':all(s['verdict']=='CERTIFIED' for s in all_summary),'problems':detailed}
    (args.output_dir/'round50_certificate.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    return 0 if result['all_six_certified'] else 2

if __name__=='__main__': raise SystemExit(main())
