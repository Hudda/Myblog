import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Post

class PostModelTests(TestCase):

    def test_was_published_recently_with_future_post(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_post = Post(pub_date=time)
        self.assertIs(future_post.was_published_recently(), False)

    def test_was_published_recently_with_past_post(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        past_post = Post(pub_date=time)
        self.assertIs(past_post.was_published_recently(), False)

    def test_was_published_recently_with_recent_post(self):
        time = timezone.now() - datetime.timedelta(minutes=59, seconds=59)
        recent_post = Post(pub_date=time)
        self.assertIs(recent_post.was_published_recently(), True)


def create_post(topic_text, days):
    pub_date = timezone.now() + datetime.timedelta(days=days)
    return Post.objects.create(
        topic_text=topic_text, pub_date=pub_date
    )


class PostIndexViewTests(TestCase):

    def test_no_post(self):
        response = self.client.get(reverse('blog:index'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'No posts are available.')
        self.assertQuerysetEqual(response.context['latest_post_list'], [])

    def test_past_post(self):
        past_post = create_post(topic_text="Past post", days=-30)
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            ['<Post: Past post>']
        )

    def test_future_post(self):
        future_post = create_post(topic_text='Future post', days=30)
        response = self.client.get(reverse('blog:index'))
        self.assertContains(response, 'No posts are available.')
        self.assertQuerysetEqual(response.context['latest_post_list'], [])

    def test_past_post_and_future_post(self):
        future_post = create_post(topic_text='Future post', days=30)
        past_post = create_post(topic_text='Past post', days=-30)
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            ['<Post: Past post>']
        )

    def test_two_past_post(self):
        past_post_1 = create_post(topic_text='Past post 1', days=-30)
        past_post_2 = create_post(topic_text='Past post 2', days=-5)
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            ['<Post: Past post 2>', '<Post: Past post 1>']
        )


class PostDetailViewTests(TestCase):

    def test_past_post(self):
        past_post = create_post(topic_text="Past post", days=-4)
        url = reverse('blog:detail', args=(past_post.id,))
        response = self.client.get(url)
        self.assertContains(response, past_post.topic_text)

    def test_future_post(self):
        future_post = create_post(topic_text="Future post", days = 4)
        url = reverse('blog:detail', args=(future_post.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class CommentViewTests(TestCase):

    def test_