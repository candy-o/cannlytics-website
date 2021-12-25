"""
Videos Views | Cannlytics Website
Copyright (c) 2021 Cannlytics

Authors: Keegan Skeate <keegan@cannlytics.com>
Created: 11/15/2021
Updated: 11/24/2021
License: MIT License <https://github.com/cannlytics/cannlytics-website/blob/main/LICENSE>
"""
# Standard imports
from math import ceil
from random import randint

# External imports.
from django.views.generic import TemplateView

# Internal imports
from cannlytics.auth.auth import authenticate_request
from cannlytics.firebase import get_document, get_collection
from website.views.mixins import BaseMixin


class VideosView(BaseMixin, TemplateView):
    """Videos page with pagination. Single videos
    load with 3 random more videos and 3 recent videos.
    """

    def get_template_names(self):
        return ['website/pages/videos/videos.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        video_id = self.kwargs.get('video_id', '')

        # Get video data.
        video_stats = get_document('public/videos')
        total_videos = video_stats['total_videos']

        # Get specific video data.
        if video_id:
            context['video_data'] = get_document(f'public/videos/video_data/{video_id}')

            # Get more videos.
            more_videos = []
            try:
                while len(more_videos) < 3:
                    random_number = randint(1, total_videos)
                    if random_number == context['video_data']['number']:
                        continue
                    random_video = get_collection(
                        'public/videos/video_data',
                        limit=1,
                        order_by='number',
                        desc=True,
                        start_at={'key': 'number', 'value': random_number }
                    )
                    more_videos = [*more_videos, *random_video]
            except:
                pass

            # Get recent videos.
            try:
                context['recent_videos'] = get_collection(
                    'public/videos/video_data',
                    limit=3,
                    order_by='number',
                    desc=True,
                    start_at={'key': 'number', 'value': total_videos + 1}
                )
                context['more_videos'] = more_videos
            except:
                pass

            # Handle sign-in for premium videos.
            if context.get('premium') or True:
                claims, _, _ = authenticate_request(self.request)
                context['user_id'] = claims.get('user_id')
                print('User ID:', context['user_id'])

                # TODO: Look-up if user has a subscription.
                context['premium_subscription'] = False

            return context

        # Paginate videos.
        limit = 9
        page = self.request.GET.get('page', 1)
        start_at = 1 + total_videos - (int(page) - 1) * limit
        context['page_index'] = range(ceil(total_videos / 10))
        context['last_page'] = str(context['page_index'][-1] + 1)
        context['video_archive'] = get_collection(
            'public/videos/video_data',
            limit=limit,
            order_by='number',
            desc=True,
            start_at={'key': 'number', 'value': start_at }
        )
        return context
