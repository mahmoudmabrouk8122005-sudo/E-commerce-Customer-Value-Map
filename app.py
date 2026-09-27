"""E-commerce Customer Value Map — Tkinter RFM analytics app."""
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Retail Radar: coral, cobalt, and cream with a customer-value focused layout.
CORAL='#D95D57'; NAVY='#172B4D'; CREAM='#FFF9F3'; BLUE='#3972AC'; MUTED='#77849A'
class RetailRadar(tk.Tk):
    def __init__(self):
        super().__init__(); self.title('E-commerce Customer Value Map'); self.geometry('1300x820'); self.configure(bg=CREAM)
        base=Path(__file__).parent/'data'; self.sales=pd.read_csv(base/'monthly_sales.csv'); self.rfm=pd.read_csv(base/'customer_rfm.csv'); self.sales['Year']=self.sales['Month'].astype(str).str[:4]; self.start_year=tk.StringVar(); self.end_year=tk.StringVar(); self.segment_var=tk.StringVar(value='Platinum'); self.build(); self.render()
    def build(self):
        top=tk.Frame(self,bg=CREAM,padx=34,pady=22); top.pack(fill='x'); tk.Label(top,text='RETAIL RADAR',bg=CREAM,fg=NAVY,font=('Segoe UI',12,'bold')).pack(side='left'); tk.Label(top,text='CUSTOMER INTELLIGENCE / 03',bg=CREAM,fg=MUTED,font=('Consolas',9)).pack(side='right')
        tk.Frame(self,bg=CORAL,height=4).pack(fill='x',padx=34)
        hero=tk.Frame(self,bg=CREAM,padx=34,pady=24); hero.pack(fill='x'); tk.Label(hero,text='Value is a behavior.',bg=CREAM,fg=CORAL,font=('Georgia',35,'italic')).pack(anchor='w'); tk.Label(hero,text='Map the customers behind repeat revenue with a practical RFM view.',bg=CREAM,fg=NAVY,font=('Segoe UI',11)).pack(anchor='w',pady=(6,0))
        self.metrics=tk.Frame(self,bg=CREAM,padx=34); self.metrics.pack(fill='x'); self.labels=[]
        for i in range(3):
            f=tk.Frame(self.metrics,bg='white',highlightbackground='#E8DCD4',highlightthickness=1,padx=18,pady=13); f.pack(side='left',fill='both',expand=True,padx=(0 if i==0 else 10,0)); a=tk.Label(f,text='—',bg='white',fg=MUTED,font=('Consolas',8)); a.pack(anchor='w'); b=tk.Label(f,text='—',bg='white',fg=CORAL,font=('Georgia',23,'bold')); b.pack(anchor='w',pady=5); self.labels.append((a,b))
        years=sorted(self.sales.Year.unique()); self.start_year.set(years[0]); self.end_year.set(years[-1]); controls=tk.Frame(self,bg=CREAM,padx=34); controls.pack(fill='x'); tk.Label(controls,text='COMPARE REVENUE YEARS',bg=CREAM,fg=MUTED,font=('Consolas',9)).pack(side='left'); ttk.Combobox(controls,textvariable=self.start_year,values=years,state='readonly',width=10).pack(side='left',padx=10); tk.Label(controls,text='vs',bg=CREAM,fg=MUTED).pack(side='left'); ttk.Combobox(controls,textvariable=self.end_year,values=years,state='readonly',width=10).pack(side='left',padx=10); tk.Label(controls,text='SEGMENT',bg=CREAM,fg=MUTED,font=('Consolas',9)).pack(side='left',padx=(24,6)); ttk.Combobox(controls,textvariable=self.segment_var,values=sorted(self.rfm.Segment.dropna().unique().tolist()),state='readonly',width=12).pack(side='left'); main=tk.Frame(self,bg=CREAM,padx=34,pady=20); main.pack(fill='both',expand=True); left=tk.Frame(main,bg='white',highlightbackground='#E8DCD4',highlightthickness=1,padx=14); left.pack(side='left',fill='both',expand=True,padx=(0,10)); right=tk.Frame(main,bg='white',highlightbackground='#E8DCD4',highlightthickness=1,padx=14); right.pack(side='left',fill='both',expand=True); tk.Label(left,text='MONTHLY REVENUE',bg='white',fg=MUTED,font=('Consolas',9)).pack(anchor='w'); tk.Label(right,text='CUSTOMER VALUE SEGMENTS',bg='white',fg=MUTED,font=('Consolas',9)).pack(anchor='w')
        self.fig=Figure(figsize=(6,4),dpi=100,facecolor='white'); self.ax=self.fig.add_subplot(111); self.canvas=FigureCanvasTkAgg(self.fig,master=left); self.canvas.get_tk_widget().pack(fill='both',expand=True)
        self.fig2=Figure(figsize=(5,4),dpi=100,facecolor='white'); self.ax2=self.fig2.add_subplot(111); self.canvas2=FigureCanvasTkAgg(self.fig2,master=right); self.canvas2.get_tk_widget().pack(fill='both',expand=True)
        self.result_frame=tk.Frame(self,bg='#FFF0EA',padx=34,pady=12); self.result_frame.pack(fill='x',padx=34); self.result_label=tk.Label(self.result_frame,text='Press SEGMENT CUSTOMERS to identify the highest-value group.',bg='#FFF0EA',fg=NAVY,font=('Segoe UI',10,'bold')); self.result_label.pack(side='left'); tk.Button(self.result_frame,text='COMPARE YEARS',command=self.compare_years,bg=CORAL,fg='white',relief='flat',font=('Segoe UI',9,'bold'),padx=12).pack(side='right'); tk.Button(self.result_frame,text='PROFILE SEGMENT',command=self.profile_segment,bg=BLUE,fg='white',relief='flat',font=('Segoe UI',9,'bold'),padx=12).pack(side='right',padx=8); tk.Label(self,bg=CREAM,fg=MUTED,text='RFM = Recency · Frequency · Monetary  |  Source: UCI Online Retail',font=('Consolas',9),pady=9).pack()
    def render(self):
        self.labels[0][0].config(text='REVENUE MAPPED'); self.labels[0][1].config(text=f"£{self.sales.Revenue.sum()/1e6:.1f}M"); self.labels[1][0].config(text='CUSTOMERS PROFILED'); self.labels[1][1].config(text=f'{len(self.rfm):,}'); self.labels[2][0].config(text='MONTHS TRACKED'); self.labels[2][1].config(text=str(len(self.sales)))
        self.ax.clear(); self.ax.plot(self.sales.Month,self.sales.Revenue,color=CORAL,marker='o',lw=2.5); self.ax.set_title('Revenue movement',loc='left',fontdict={'fontsize':14,'fontweight':'bold','color':NAVY}); self.ax.tick_params(axis='x',rotation=45,labelsize=7); self.ax.grid(alpha=.15,axis='y'); self.ax.spines[['top','right']].set_visible(False)
        seg=self.rfm.groupby('Segment',observed=False).Monetary.sum().sort_values(); self.ax2.clear(); self.ax2.barh(seg.index,seg.values,color=BLUE); self.ax2.set_title('Total value by segment',loc='left',fontdict={'fontsize':14,'fontweight':'bold','color':NAVY}); self.ax2.tick_params(labelsize=8); self.ax2.grid(alpha=.15,axis='x'); self.ax2.spines[['top','right']].set_visible(False); self.fig.tight_layout(); self.fig2.tight_layout(); self.canvas.draw(); self.canvas2.draw()
    def segment_customers(self):
        if self.rfm.empty: return
        group=self.rfm.groupby('Segment',observed=False).agg(Customers=('CustomerID','count'),Revenue=('Monetary','sum')).sort_values('Revenue',ascending=False); best=group.index[0]
        self.result_label.config(text=f'SEGMENT RESULT  →  {best} customers represent the strongest revenue pool with £{group.iloc[0].Revenue:,.0f} mapped value across {int(group.iloc[0].Customers):,} profiles.')

    def compare_years(self):
        a=self.sales[self.sales.Year==self.start_year.get()].Revenue.sum(); b=self.sales[self.sales.Year==self.end_year.get()].Revenue.sum(); diff=b-a; pct=(diff/a*100) if a else 0
        self.result_label.config(text=f'YEAR COMPARISON  →  {self.start_year.get()} = £{a:,.0f}  |  {self.end_year.get()} = £{b:,.0f}  |  Change = £{diff:+,.0f} ({pct:+.1f}%).')

    def profile_segment(self):
        d=self.rfm[self.rfm.Segment==self.segment_var.get()]; self.result_label.config(text=f'SEGMENT RESULT → {self.segment_var.get()} has {len(d):,} customers, average monetary value £{d.Monetary.mean():,.0f}, and average frequency {d.Frequency.mean():.1f}. Recommendation: build a retention offer around this segment.')

if __name__=='__main__': RetailRadar().mainloop()
