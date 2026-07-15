#!/usr/bin/env python3
import argparse,csv,sys
from pathlib import Path
import mpmath as mp
sys.path.insert(0,str(Path(__file__).resolve().parent))
import round50_krawczyk_certifier as rc

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--nodes-csv',type=Path,required=True); ap.add_argument('--alternation-csv',type=Path,required=True); ap.add_argument('--output',type=Path,required=True); a=ap.parse_args()
 mp.mp.dps=100; rows=[]
 for n,k in rc.PROBLEMS:
  z0,s=rc.load_center(a.nodes_csv,a.alternation_csv,n,k)
  z,f,J,h=rc.refine(z0,n,k,s,mp.mpf('1e-80'))
  N=len(z); maxabs=mp.mpf(0); maxrel=mp.mpf(0); wi=wj=-1
  for col in range(N):
   for row in range(N):
    def g(t):
     zz=mp.matrix(z); zz[col]=t
     return rc.eval_mp(zz,n,k,s)[0][row]
    num=mp.diff(g,z[col]); ana=J[row,col]; ad=abs(num-ana); rd=ad/max(mp.mpf(1),abs(num),abs(ana))
    if ad>maxabs: maxabs=ad; wi=row; wj=col
    maxrel=max(maxrel,rd)
  rows.append({'n':n,'k':k,'unknowns':N,'max_absolute_difference':mp.nstr(maxabs,20),'max_scaled_difference':mp.nstr(maxrel,20),'worst_row':wi,'worst_column':wj,'verdict':'PASS' if maxrel<mp.mpf('1e-80') else 'REVIEW'})
 with a.output.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 for r in rows: print(r)
if __name__=='__main__': main()
