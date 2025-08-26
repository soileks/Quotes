from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import F
from random import choices
from django.contrib import messages
from .models import Quote, Source
from .forms import QuoteForm, SourceForm



def random_quote(request):
    try:
        quotes = Quote.objects.all()

        if quotes:
            weights = [quote.weight for quote in quotes]
            selected_quote = choices(list(quotes), weights=weights, k=1)[0]
            selected_quote.views_count += 1
            selected_quote.save()
        else:
            selected_quote = None

        total_quotes = quotes.count()

    except:
        # Если база данных не доступна
        selected_quote = None
        total_quotes = 0
        messages.warning(request, 'База данных не готова. Добавьте первые цитаты.')

    return render(request, 'quotes/random_quote.html', {
        'quote': selected_quote,
        'total_quotes': total_quotes
    })


def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Цитата успешно добавлена!')
                return redirect('random_quote')
            except Exception as e:
                messages.error(request, f'Ошибка: {str(e)}')
    else:
        form = QuoteForm()

    return render(request, 'quotes/add_quote.html', {'form': form})


def add_source(request):
    if request.method == 'POST':
        form = SourceForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Источник успешно добавлен!')
                return redirect('add_quote')
            except Exception as e:
                messages.error(request, f'Ошибка: {str(e)}')
    else:
        form = SourceForm()

    return render(request, 'quotes/add_source.html', {'form': form})


def like_quote(request, quote_id):
    if request.method == 'POST':
        try:
            quote = get_object_or_404(Quote, id=quote_id)
            quote.likes += 1
            quote.save()
            return JsonResponse({
                'likes': quote.likes,
                'dislikes': quote.dislikes,
                'rating': quote.rating
            })
        except:
            return JsonResponse({'error': 'Database error'})
    return JsonResponse({'error': 'Invalid request'})


def dislike_quote(request, quote_id):
    if request.method == 'POST':
        try:
            quote = get_object_or_404(Quote, id=quote_id)
            quote.dislikes += 1
            quote.save()
            return JsonResponse({
                'likes': quote.likes,
                'dislikes': quote.dislikes,
                'rating': quote.rating
            })
        except:
            return JsonResponse({'error': 'Database error'})
    return JsonResponse({'error': 'Invalid request'})


def top_quotes(request):
    try:
        from django.db.models import ExpressionWrapper, IntegerField

        top_by_rating = Quote.objects.annotate(
            rating_value=ExpressionWrapper(F('likes') - F('dislikes'), output_field=IntegerField())
        ).order_by('-rating_value')[:10]


        top_by_views = Quote.objects.order_by('-views_count')[:10]
        top_by_likes = Quote.objects.order_by('-likes')[:10]
        top_by_weight = Quote.objects.order_by('-weight')[:10]

        return render(request, 'quotes/top_quotes.html', {
            'top_by_rating': top_by_rating,
            'top_by_views': top_by_views,
            'top_by_likes': top_by_likes,
            'top_by_weight': top_by_weight,
            'source_stats': [],
        })

    except Exception as e:
        print(f"Error in top_quotes: {e}")

        quotes = list(Quote.objects.all())
        return render(request, 'quotes/top_quotes.html', {
            'top_by_rating': sorted(quotes, key=lambda x: x.rating, reverse=True)[:10],
            'top_by_views': sorted(quotes, key=lambda x: x.views_count, reverse=True)[:10],
            'top_by_likes': sorted(quotes, key=lambda x: x.likes, reverse=True)[:10],
            'top_by_weight': sorted(quotes, key=lambda x: x.weight, reverse=True)[:10],
            'source_stats': [],
        })