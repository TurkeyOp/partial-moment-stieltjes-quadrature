#!/usr/bin/env python3
"""Rigorous global alternation audit on the certified Round-50 root boxes.

For each exact root guaranteed by Krawczyk, this script proves the sign of
relative-error derivative between consecutive certified extrema, and the
sign of the second derivative in a neighborhood of each internal extremum.
Together with the exact square-system equations, this proves that the
alternating level E is the global uniform relative-error norm on [0.08,0.12].
"""
from __future__ import annotations
import argparse,csv,json,sys
from pathlib import Path
import mpmath as mp
from flint import arb,ctx
sys.path.insert(0,str(Path(__file__).resolve().parent))
import round50_krawczyk_certifier as rc


def make_interval(left,right):
    return arb(mp.nstr((left+right)/2,80),mp.nstr((right-left)/2,40))


def eps_derivatives(y,w,b):
    F=rc.arb_f0(b); Fb=rc.arb_f1(b); Fbb=rc.arb_f2(b)
    D=[b*b+y[j] for j in range(len(y))]
    r=2*sum((w[j]/D[j] for j in range(len(y))),arb(0))
    rb=-4*b*sum((w[j]/D[j]**2 for j in range(len(y))),arb(0))
    rbb=-4*sum((w[j]/D[j]**2 for j in range(len(y))),arb(0))+16*b*b*sum((w[j]/D[j]**3 for j in range(len(y))),arb(0))
    eb=(rb*F-r*Fb)/(F**2)
    ebb=rbb/F-r*Fbb/(F**2)-2*rb*Fb/(F**2)+2*r*Fb*Fb/(F**3)
    return eb,ebb


def certify_derivative_sign(y,w,left,right,expected,max_depth=45):
    stack=[(left,right,0)]; leaves=0; visited=0; depth_used=0; min_margin=None
    while stack:
        l,r,dep=stack.pop(); visited+=1; depth_used=max(depth_used,dep)
        eb,_=eps_derivatives(y,w,make_interval(l,r))
        margin=float(eb.lower()) if expected>0 else float(-eb.upper())
        if margin>0:
            leaves+=1; min_margin=margin if min_margin is None else min(min_margin,margin); continue
        if dep>=max_depth:
            return {'certified':False,'visited':visited,'leaves':leaves,'max_depth':depth_used,'minimum_signed_margin':min_margin,'failure_left':mp.nstr(l,40),'failure_right':mp.nstr(r,40),'failure_interval':str(eb)}
        mid=(l+r)/2
        stack.append((mid,r,dep+1)); stack.append((l,mid,dep+1))
    return {'certified':True,'visited':visited,'leaves':leaves,'max_depth':depth_used,'minimum_signed_margin':min_margin}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--nodes-csv',type=Path,required=True); ap.add_argument('--alternation-csv',type=Path,required=True); ap.add_argument('--output-dir',type=Path,required=True); ap.add_argument('--neighborhood-halfwidth',default='1e-5'); a=ap.parse_args()
    a.output_dir.mkdir(parents=True,exist_ok=True); mp.mp.dps=180;ctx.dps=180; hw=mp.mpf(a.neighborhood_halfwidth)
    summaries=[]; segment_rows=[]; curvature_rows=[]; details={}
    for n,k in rc.PROBLEMS:
        z0,signs=rc.load_center(a.nodes_csv,a.alternation_csv,n,k)
        z,f,J,hist=rc.refine(z0,n,k,signs,mp.mpf('1e-140'))
        cert=rc.certify(z,J,n,k,signs,12)
        if not cert['success']: raise RuntimeError(f'Nested Krawczyk box failed for {(n,k)}')
        X=cert['X']; y=X[:n];w=X[n:2*n];q=2*n-k-1
        centers=[z[2*n+i] for i in range(q)]
        neighborhoods=[]
        for i,c in enumerate(centers):
            l=c-hw;r=c+hw
            if l<=mp.mpf('0.08') or r>=mp.mpf('0.12'): raise RuntimeError('Neighborhood leaves structural interval')
            if i and l<=neighborhoods[-1][1]: raise RuntimeError('Overlapping extremum neighborhoods')
            neighborhoods.append((l,r))
        all_ok=True; total_visited=0; total_leaves=0; maximum_depth=0; min_deriv=None
        boundaries=[mp.mpf('0.08')]
        for l,r in neighborhoods: boundaries.extend([l,r])
        boundaries.append(mp.mpf('0.12'))
        # macro derivative segments: endpoint->N1, N1->N2, ..., Nq->endpoint
        macro=[]; current=mp.mpf('0.08')
        for i,(l,r) in enumerate(neighborhoods):
            macro.append((current,l,i));current=r
        macro.append((current,mp.mpf('0.12'),q))
        for left,right,between_index in macro:
            expected=1 if signs[between_index+1]>signs[between_index] else -1
            out=certify_derivative_sign(y,w,left,right,expected)
            all_ok &= out['certified']; total_visited+=out['visited'];total_leaves+=out['leaves'];maximum_depth=max(maximum_depth,out['max_depth'])
            md=out.get('minimum_signed_margin'); min_deriv=md if min_deriv is None else min(min_deriv,md if md is not None else min_deriv)
            segment_rows.append({'n':n,'k':k,'segment_index':between_index,'left':mp.nstr(left,50),'right':mp.nstr(right,50),'expected_derivative_sign':expected,**out})
        min_curv=None
        for i,(left,right) in enumerate(neighborhoods):
            _,ebb=eps_derivatives(y,w,make_interval(left,right)); expected=-signs[i+1]
            margin=float(ebb.lower()) if expected>0 else float(-ebb.upper()); ok=margin>0;all_ok &= ok
            min_curv=margin if min_curv is None else min(min_curv,margin)
            curvature_rows.append({'n':n,'k':k,'internal_extremum_index':i+1,'left':mp.nstr(left,50),'right':mp.nstr(right,50),'extremum_error_sign':signs[i+1],'expected_second_derivative_sign':expected,'second_derivative_lower':str(ebb.lower()),'second_derivative_upper':str(ebb.upper()),'signed_margin':margin,'certified':ok})
        summary={'n':n,'k':k,'nested_box_radius':'1e-12','krawczyk_certified':cert['success'],'derivative_segments_certified':all(r['certified'] for r in segment_rows if r['n']==n and r['k']==k),'curvature_neighborhoods_certified':all(r['certified'] for r in curvature_rows if r['n']==n and r['k']==k),'global_uniform_level_certified':all_ok,'alternation_points':2*n-k+1,'internal_extrema':q,'subintervals_visited':total_visited,'certified_derivative_leaves':total_leaves,'maximum_subdivision_depth':maximum_depth,'minimum_derivative_sign_margin':min_deriv,'minimum_curvature_sign_margin':min_curv}
        summaries.append(summary);details[f'n{n}_k{k}']=summary
        print((n,k),'GLOBAL_MINIMAX_CERTIFIED' if all_ok else 'FAILED','visited',total_visited)
    with (a.output_dir/'round50_global_minimax_summary.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(summaries[0]));w.writeheader();w.writerows(summaries)
    with (a.output_dir/'round50_monotonicity_segments.csv').open('w',newline='',encoding='utf-8') as f:
        cols=[]
        for r in segment_rows:
            for c in r:
                if c not in cols: cols.append(c)
        w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(segment_rows)
    with (a.output_dir/'round50_curvature_neighborhoods.csv').open('w',newline='',encoding='utf-8') as f:
        cols=list(curvature_rows[0]) if curvature_rows else ['n','k'];w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(curvature_rows)
    result={'method':'Krawczyk root boxes plus interval derivative-sign subdivision and interval curvature signs','neighborhood_halfwidth':a.neighborhood_halfwidth,'all_six_global_uniform_levels_certified':all(s['global_uniform_level_certified'] for s in summaries),'problems':details}
    (a.output_dir/'round50_global_minimax_audit.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    return 0 if result['all_six_global_uniform_levels_certified'] else 2
if __name__=='__main__': raise SystemExit(main())
