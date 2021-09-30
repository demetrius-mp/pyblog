$('#posts').on('click', '.like', (e) => {
  const postId = parseInt(e.target.id)
  const was_liked = e.target.classList.contains('bi-hand-thumbs-up-fill')
  const request_method = was_liked ? 'DELETE' : 'POST'
  $.ajax({
    url: `api/likes/${postId}`,
    type: request_method,
    success: () => {
      const is_liked = !was_liked
      const $likesCount = $(`#likesCount_${postId}`)
      const likesCount = parseInt($likesCount.text())
      
      if (is_liked) {
        $likesCount.text(likesCount + 1)
        e.target.classList.remove('bi-hand-thumbs-up')
        e.target.classList.add('bi-hand-thumbs-up-fill')
      }
      else {
        $likesCount.text(likesCount - 1)
        e.target.classList.remove('bi-hand-thumbs-up-fill')
        e.target.classList.add('bi-hand-thumbs-up')
      }
    },
    error: (data) => {
      const statusCode = data['status']
      if (statusCode === 401 || statusCode === 400) {
        const r = data['responseJSON']
        showToast(r['category'], r['msg'])
      }
    }
  })
})