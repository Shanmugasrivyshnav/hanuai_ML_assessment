"""Visible, conservative collector for public Best Buy Canada review pages. No access-control evasion."""
import argparse,csv,hashlib,re,time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
SORTS=['Most Helpful','Newest','Highest Rating','Lowest Rating','Most Relevant']
# Update selectors only after inspecting the current public page.
SEL={'card':'[data-testid*="review"], .review-item, [class*="reviewItem"]','title':'[data-testid*="title"], [class*="reviewTitle"], h3','body':'[data-testid*="text"], [class*="reviewText"], [class*="reviewBody"]','date':'time, [class*="reviewDate"]','name':'[class*="reviewer"], [class*="userName"]','rating':'[aria-label*="out of 5"], [class*="rating"]','more':'button:has-text("Show More"), button:has-text("Load More")'}
def txt(node,sel):
 x=node.locator(sel).first
 return re.sub(r'\\s+',' ',x.inner_text(timeout=1000)).strip() if x.count() else ''
def dateval(s):
 s=(s or '').strip()
 for f in ('%B %d, %Y','%b %d, %Y','%Y-%m-%d','%m/%d/%Y'):
  try:return datetime.strptime(s,f).date().isoformat()
  except ValueError:pass
 m=re.search(r'\\d{4}-\\d{2}-\\d{2}',s); return m.group() if m else ''
def scrape(url,out,max_clicks=30,delay=2):
 if urlparse(url).hostname not in ('bestbuy.ca','www.bestbuy.ca'): raise ValueError('Only bestbuy.ca URLs allowed')
 rows={}
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=False); page=browser.new_page(locale='en-CA'); page.goto(url,wait_until='domcontentloaded',timeout=60000)
  input('Handle any ordinary consent prompt manually; when public reviews are visible press Enter: ')
  for sort in SORTS:
   try:
    ctl=page.get_by_role('button',name=re.compile('sort|filter',re.I)).first
    if ctl.count():
     ctl.click(timeout=1500); opt=page.get_by_text(sort,exact=False).last
     if opt.count():opt.click(timeout=1500); page.wait_for_timeout(1200)
   except Exception:pass
   for _ in range(max_clicks+1):
    cards=page.locator(SEL['card'])
    for i in range(cards.count()):
     c=cards.nth(i)
     try:
      title=txt(c,SEL['title']); body=txt(c,SEL['body']); de=c.locator(SEL['date']).first
      raw=(de.get_attribute('datetime') or de.inner_text()) if de.count() else ''
      na=txt(c,SEL['name']); relem=c.locator(SEL['rating']).first
      ratraw=(relem.get_attribute('aria-label') or relem.inner_text()) if relem.count() else ''
      m=re.search(r'([1-5](?:\\.\\d+)?)',ratraw); rating=float(m.group(1)) if m else ''
      key=hashlib.sha256((url+raw+na+title+body).encode()).hexdigest()[:16]
      if title or body:rows[key]=[key,title,body,dateval(raw),rating,url,na]
     except Exception:pass
    more=page.locator(SEL['more']).last
    if not more.count() or not more.is_visible():break
    try:more.click(timeout=3000)
    except Exception:break
    page.wait_for_timeout(int(delay*1000))
   time.sleep(delay)
  browser.close()
 Path(out).parent.mkdir(parents=True,exist_ok=True)
 with open(out,'w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f);w.writerow(['primary_key','title','review_text','date','rating','source','reviewer_name']);w.writerows(rows.values())
 print(f'Saved {len(rows)} unique reviews to {out}')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('url');p.add_argument('--output',default='data/bestbuy_reviews.csv');p.add_argument('--max-clicks',type=int,default=30);p.add_argument('--delay',type=float,default=2);a=p.parse_args();scrape(a.url,a.output,a.max_clicks,a.delay)
