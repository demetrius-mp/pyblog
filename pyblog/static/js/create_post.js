const easymde = new EasyMDE({
  element: document.getElementById("content"),
  renderingConfig: {
    codeSyntaxHighlighting: true
  },
  autofocus: true,
  placeholder: "Supports markdown!",
  maxHeight: "300px"
});


const $description = $('#description')
const $descriptionCharCounter = $('#descriptionCharCounter')
const $tags = $('#tags')
const $tagsCounter = $('#tagsCounter')

$description.on('input', () => {
  const numCharacters = $description.val().length
  $descriptionCharCounter.text(numCharacters)
})

$tags.on('input', (e) => {
  const numTags = $tags.val().replace(/[^#]/g, "").length
  if (numTags <= 5) {
    $tagsCounter.text(numTags)
  }
})
