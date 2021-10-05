function setPostContent(postSlug) {
  $.ajax({
    url: `/api/posts/${postSlug}`,
    type: 'GET',
    success: (data) => setText(data)
  })
}

function setText(text) {
  const element = document.getElementById('postContent')
  const sanitizedContent = DOMPurify.sanitize(text);
  element.innerHTML = marked(sanitizedContent);
}