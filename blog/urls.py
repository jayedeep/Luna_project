from django.urls import path
from . views import (PostCreate,PostListView,PostRetriveUpdateDestroy,PostListSearch,PostListFilter,
                    CategoryCreate,CategoryListView,CategoryRetriveUpdateDestroy,
                    LikesCreate,LikesListView,LikesRetriveUpdateDestroy,LikeListByUserIds)
urlpatterns = [
    path('',PostListView.as_view()),
    path('post/createpost',PostCreate.as_view()),
    path('post/<int:pk>',PostRetriveUpdateDestroy.as_view()),
    path('post/search/',PostListSearch.as_view(),name="postsearch"),
    path('post/filter/',PostListFilter.as_view(),name="postfilter"),

    path('categorylist',CategoryListView.as_view()),
    path('category/createcategory',CategoryCreate.as_view()),
    path('category/<int:pk>',CategoryRetriveUpdateDestroy.as_view()),

    path('likelist',LikesListView.as_view()),
    path('likelist/create',LikesCreate.as_view()),
    path('likelist/<int:pk>',LikesRetriveUpdateDestroy.as_view()),
    
    path('likesbyuserids',LikeListByUserIds.as_view(),name='likebyuserids')

]