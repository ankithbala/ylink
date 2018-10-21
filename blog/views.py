from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
import youtube_dl
from django.core.files import File
from .models import FileSaver
import codecs
from django.views.static import serve
import os

def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            l=post.text
            '''
            def my_hook(d):
                if d['status'] == 'finished':
                    print('Done downloading, now converting ...')
            '''
            ydl_opts = {}
            
           
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(l, download=False)
                download_target = ydl.prepare_filename(info)
                ydl.download([l])
                
            filepath = download_target
            return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
        
        
        
            '''pdfImage = FileSaver()
           # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            #    ydl.download([l])
           
         
            local_file = codecs.open(s, "r",encoding='utf-8', errors='ignore')
            djangofile = File(local_file)
            pdfImage.myfile.save('new', djangofile)
            local_file.close()
           '''
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})



def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
