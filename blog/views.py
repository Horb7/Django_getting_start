from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from blog.models import Article
from django.core.paginator import Paginator


def hello_world(request):
    return HttpResponse("Hello World!")

def article_content(request):
    article = Article.objects.all()[0]
    title = article.title
    brief_content = article.brief_content
    content = article.content
    article_id = article.article_id
    publish_date = article.publish_date
    return_str = 'title: %s, brief_content: %s, ' \
                 'content: %s, article_id: %s, publish_date: %s' % (title,
                                                                    brief_content,
                                                                    content,
                                                                    article_id,
                                                                    publish_date)
    return HttpResponse(return_str)

def get_index_page(request):
    page = request.GET.get('page')
    # 如果没有page参数，则page为1
    if page:
        page = int(page)
    else:
        page = 1
    all_article = Article.objects.all()
    paginator = Paginator(all_article, 3)
    page_num = paginator.num_pages
    page_article_list = paginator.page(page)
    top5_article = Article.objects.order_by('-publish_date')[:5]
    if page_article_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_article_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page
    return render(request, 'blog/index.html',
                  {
                      'article_list': page_article_list,
                      'page_num': range(1, page_num + 1),
                      'curr_page': page,
                      'next_page': next_page,
                      'previous_page': previous_page,
                      'top5_article': top5_article
                  }
                  )

def get_detail_page(request, article_id):
    all_article = Article.objects.all()
    curr_article_index = None
    for index, article in enumerate(all_article):
        if article.article_id == article_id:
            curr_article_index = index
            break
    curr_article = all_article[curr_article_index]
    previous_article = all_article[curr_article_index - 1]
    next_article = all_article[curr_article_index + 1]
    if curr_article_index == 0:
        previous_article = curr_article
    if curr_article_index == len(all_article) - 1:
        next_article = curr_article
    section_list = curr_article.content.split('\n')
    return render(request, 'blog/detail.html',
                  {
                      'curr_article': curr_article,
                      'section_list': section_list,
                      'previous_article': previous_article,
                      'next_article': next_article
                  }
                  )