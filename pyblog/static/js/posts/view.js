function setPostContent(postId) {
  $.ajax({
    url: `/api/posts/${postId}`,
    type: 'GET',
    success: (data) => setText(data)
  })
}

function setText(text) {
  const element = document.getElementById('postContent')
  const sanitizedContent = DOMPurify.sanitize(text);
  element.innerHTML = marked(sanitizedContent);
}