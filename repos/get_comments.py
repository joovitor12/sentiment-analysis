import requests
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk



def get_comments():
  token = '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'

  owner = 'liferay'
  repo = 'liferay-portal'

  url_to_get_prs_number = f'https://api.github.com/repos/{owner}/{repo}/pulls?q=mergeable:conflicting'

  headers = {'Authorization': f'token {token}'}


  response = requests.get(url_to_get_prs_number, headers=None)


  if response.status_code == 200:
      prs = response.json()
      pr_numbers = [pr_number['number'] for pr_number in prs]

      all_comments = []
      nltk.download('punkt')  # Certifique-se de ter o 'punkt' instalado
      nltk.download('stopwords')
      stop_words = set(stopwords.words('english'))

      for pr_response in pr_numbers:
          url_to_get_pr_comments = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_response}/comments'
          response = requests.get(url_to_get_pr_comments, headers=headers)
          pr_comments = response.json()

          bodies = [comment['body'] for comment in pr_comments]
          
          cleaned_bodies = []
          for body in bodies:
              cleaned_words = [word for word in word_tokenize(body) if word.lower() not in stop_words]
              cleaned_bodies.append(' '.join(cleaned_words))
              
          all_comments.extend(cleaned_bodies)
      
      return all_comments
      
  else:
      print(f'Falha na solicitação: {response.status_code} - {response.text}')
      return None
