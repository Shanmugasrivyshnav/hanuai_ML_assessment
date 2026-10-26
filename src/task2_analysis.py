"""EDA, transparent phrase tagging and exploratory TF-IDF/K-Means for supplied CSV."""
import argparse,re
from pathlib import Path
import pandas as pd, matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
RULES={'Electrical issue':r'\\b(battery|power|charge|charging|electrical|wire|circuit|voltage)\\b','Component failure':r'\\b(broke|broken|crack|failed|failure|motor|bearing|pump|valve|component)\\b','Software / controls':r'\\b(software|firmware|app|update|sensor|control|error code|reset|connection|wifi)\\b','Assembly / fit':r'\\b(install|assembly|assemble|fit|loose|misalign|missing screw|instructions)\\b','Performance / quality':r'\\b(noise|vibration|leak|overheat|underperform|poor quality|defect|wear)\\b'}
def run(source,outdir,text_col=None,date_col=None,n_clusters=5):
 out=Path(outdir);out.mkdir(parents=True,exist_ok=True);df=pd.read_csv(source);df.columns=[str(c).strip() for c in df.columns]
 print('Shape',df.shape,'\\nTypes\\n',df.dtypes,'\\nMissing\\n',df.isna().sum(),'\\nDuplicate rows',df.duplicated().sum());df=df.drop_duplicates().copy()
 if not text_col:
  cand=[c for c in df if any(k in c.lower() for k in ('text','description','comment','review','problem','issue','narrative'))]
  text_col=max(cand,key=lambda c:df[c].fillna('').astype(str).str.len().mean()) if cand else None
 if not text_col:raise ValueError('No free text detected; pass --text-col')
 df[text_col]=df[text_col].fillna('').astype(str).str.strip()
 df['mined_entities']=df[text_col].str.lower().apply(lambda s:'; '.join(k for k,v in RULES.items() if re.search(v,s)))
 df['issue_category']=df.mined_entities.apply(lambda s:s.split('; ')[0] if s else 'Other / review needed');df['topic_cluster']=-1;terms=[]
 n=sum(bool(x.strip()) for x in df[text_col])
 if n>=max(3,n_clusters):
  vec=TfidfVectorizer(stop_words='english',max_features=3000,ngram_range=(1,2));X=vec.fit_transform(df[text_col]);labels=KMeans(n_clusters=min(n_clusters,n-1),random_state=42,n_init=10).fit_predict(X);df.topic_cluster=labels;vocab=vec.get_feature_names_out()
  for k in sorted(set(labels)):
   mean=X[labels==k].mean(axis=0).A1;terms.append({'topic_cluster':int(k),'top_terms':', '.join(vocab[mean.argsort()[-8:][::-1]])})
 df.to_csv(out/'task2_enriched.csv',index=False,encoding='utf-8-sig');df.isna().sum().rename('missing_count').to_csv(out/'missingness.csv');df.describe(include='all').T.to_csv(out/'summary_statistics.csv');df.issue_category.value_counts().to_csv(out/'issue_category_counts.csv',header=['count']);pd.DataFrame(terms).to_csv(out/'cluster_terms.csv',index=False)
 df.issue_category.value_counts().plot.bar(title='Issue categories');plt.tight_layout();plt.savefig(out/'issue_categories.png',dpi=160);plt.close()
 if date_col and date_col in df:pd.to_datetime(df[date_col],errors='coerce').dt.to_period('M').astype(str).value_counts().sort_index().to_csv(out/'monthly_counts.csv')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--outdir',default='outputs/task2');p.add_argument('--text-col');p.add_argument('--date-col');p.add_argument('--clusters',type=int,default=5);a=p.parse_args();run(a.input,a.outdir,a.text_col,a.date_col,a.clusters)
