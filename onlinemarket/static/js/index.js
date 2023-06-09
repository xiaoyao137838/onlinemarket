function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrfToken = getCookie('csrftoken')

$('.submit-like').on('click', function() {
    create_like.call(this, like_update_view, error_func);
});

function create_like(success, error) {
    let post_id = $(this).siblings('.hidden-data').find('.post-pk').text();
    console.log('like is clicked', post_id)
    $.ajax({
        type: 'POST',
        url: '/postsharing/add_like/',
        data: {
            post_id: post_id,
            'csrfmiddlewaretoken': csrfToken
        },
        success: success,
        error: error
    });
}

function like_update_view(data) {
    console.log(data)
    const {result, post_id} = data; 
    let $hiddenData = $('.hidden-data.' + post_id);
    if (result) {
        $hiddenData.siblings('.submit-like').removeClass('fa-heart-o').addClass('fa-heart');
        
    } else {
        $hiddenData.siblings('.submit-like').removeClass('fa-heart').addClass('fa-heart-o');
    }

    let $post = $('.view-update.' + post_id);
    let $likes = $post.find('.likes');
    let like_count = parseInt($likes.text());
    let diff = result ? 1 : -1;
    
    if (!like_count || isNaN(like_count)) {
        $likes.text('1 like');
    } else if (like_count == 1 && diff == -1) {
        $likes.text('');
    } else if (like_count + diff == 1) {
        $likes.text('1 like');
    } else {
        count = like_count + diff;
        $likes.text(count + ' likes');
    }
}

function error_func(error) {
    console.log(error);
}

// Add Comment
$('.add-comment').on('keyup', function(e) {
    if (enterPressed(e)) {
        if (validateComment($(this).val())) {
            create_comment.call(this, comment_update_view, error_func);
        }
    }
});

enterPressed = e => e.key == 'Enter' ? true : false;

validateComment = value => value == '' ? false : true;

function create_comment(success, error) {
    let content = $(this).val();
    let post_id = $(this).parent().siblings('.hidden-data').find('.post-pk').text();

    $.ajax({
        type: 'POST',
        url: '/postsharing/add_comment/',
        data: {
            post_id: post_id,
            content: content,
            'csrfmiddlewaretoken': csrfToken
        },
        success: success,
        error: error
    });
}

function comment_update_view(data) {
    console.log(data)
    const {result, post_id, comment_info} = data;
    let $post = $('.hidden-data.' + post_id);
    let element = `<li class="comment-list__comment"><a class="user" href="">${comment_info.user}</a> <span>${comment_info.comment}</span></li>`;
    $post.closest('.view-update').find('.comment-list').append(element);
    $('.add-comment').val('');
}

// Follow/unfollow
$('.follow-toggle__container').on('click', '.follow-user', function() {
    follow_user.call(this, update_follow_view, error_func, 'follow');
});

$('.follow-toggle__container').on('click', '.unfollow-user', function() {
    follow_user.call(this, update_unfollow_view, error_func, 'unfollow');
});

function follow_user(success, error, type) {
    let user_id = $(this).attr('id');
    console.log('follow/unfollow is clicked', user_id)

    $.ajax({
        type: 'POST',
        url: '/postsharing/toggle_connection/',
        data: {
            user_id: user_id,
            type: type,
            'csrfmiddlewaretoken': csrfToken
        },
        success: success,
        error: error
    });
}

function update_follow_view(data) {
    console.log('If follow: ', data)
    const {result, type, user_id} = data;
    let $button = $('.follow-toggle__container .btn');
    $button.addClass('unfollow-user').removeClass('follow-user');
    $button.text('Unfollow');

    let $span = $('.follower_count');
    let count = parseInt(document.getElementById('follower_id').innerText);
    console.log(count)
    $span.text(count + 1);
}

function update_unfollow_view(data) {
    console.log('If unfollow: ', data)
    const {result, type, user_id} = data;
    let $button = $('.follow-toggle__container .btn');
    $button.removeClass('unfollow-user').addClass('follow-user');
    $button.text('Follow');

    let $span = $('.follower_count');
    let count = parseInt(document.getElementById('follower_id').innerText);
    console.log(count)
    $span.text(count - 1);
}
