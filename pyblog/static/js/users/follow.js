$('#profileCard').on('click', '.follow', (e) => {
  const username = e.target.id.split('_')[1]
  const was_following = e.target.classList.contains('btn-outline-danger')
  const request_method = was_following ? 'DELETE' : 'POST'
  $.ajax({
    url: `/api/follows/${username}`,
    type: request_method,
    success: () => {
      const is_following = !was_following

      if (is_following) {
        e.target.classList.remove('btn-primary')
        e.target.classList.add('btn-outline-danger')
        e.target.innerText = 'Unfollow'
      }
      else {
        e.target.classList.remove('btn-outline-danger')
        e.target.classList.add('btn-primary')
        e.target.innerText = 'Follow'
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