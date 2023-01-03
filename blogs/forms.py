from django import forms
from blogs.models import Post, Comment

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['author'].label = "Blog Author"
            self.fields['title'].label = "Blog Title"
            self.fields['post_label'].label = "Choose Category (Post label)"
            self.fields['blog_cover_image'].label = "Choose Blog Cover Photo"
            self.fields['text'].label = "Start Content Entry"



    class Meta():
        model = Post
        fields = ('author', 'title', 'post_label', 'blog_cover_image', 'text',)

        widgets = {
            'author':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Author...'}),
            'title':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title...'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'}),
            'post_label': forms.Select(attrs={'class': 'form-control', 'placeholder':'Label it as...'}),
            'blog_cover_image':forms.FileInput(attrs={'class':'form-control buttonLabels'}),
        }



class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('text',)

        widgets = {
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }
