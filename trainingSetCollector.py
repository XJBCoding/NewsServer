from newsapi import NewsApiClient
import goose3

def collect(label,top_headlines,n):
    for obj in top_headlines['articles']:
#        g = goose3.Goose({'enable_image_fetching': False})
        g = goose3.Goose()
        goose_obj = g.extract(url=obj['url'])
        body_text = goose_obj.cleaned_text
        if body_text :
            with open('/Users/siyangyin/Desktop/testSet/'+label+'/'+str(index[n])+'.txt','w') as f:
                f.write(body_text)
                index[n]+=1

newsapi=NewsApiClient(api_key='55ba7ad3fa444f5398a1d476cbf42b02')
index=[1]*7
label=['business','entertainment','sports','technology','health','science','general']

for number in range(6,3,-1):#{'business','entertainment','sports','technology','health','sciece','general'}:
    for pageNumber in range(1,11):
        for countryKind in {'gb','us','au','ca'}:
            top_headlines=newsapi.get_top_headlines(page=pageNumber,category=label[number],country=countryKind)
            collect(label[number],top_headlines,number)

