"""VADER sentiment and interpretable aspect tag helper."""
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
_ANALYZER=SentimentIntensityAnalyzer()
def classify(text,rating=None):
 s=str(text or '').lower(); score=_ANALYZER.polarity_scores(s)['compound']
 polarity='Positive' if score>=.05 else 'Negative' if score<=-.05 else 'Neutral'
 if polarity=='Neutral' and rating not in ('',None):
  try: polarity='Positive' if float(rating)>=4 else 'Negative' if float(rating)<=2 else 'Neutral'
  except (ValueError,TypeError):pass
 for aspect,pattern in [('Design & Quality',r'design|quality|look|build'),('Performance',r'work|perform|power|fast|slow'),('Value',r'price|value|worth'),('Ease of Use',r'easy|difficult|install|setup'),('Reliability',r'broke|fail|defect|reliable')]:
  if re.search(pattern,s):break
 else:aspect='Overall Experience'
 suffix={'Positive':'Pos','Negative':'Neg','Neutral':'Neutral'}[polarity]
 return polarity,f'{aspect} ({suffix})',score
