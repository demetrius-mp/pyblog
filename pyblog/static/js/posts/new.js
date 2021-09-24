const easymde = new EasyMDE({
  element: document.getElementById("content"),
  renderingConfig: {
    codeSyntaxHighlighting: true
  },
  autofocus: true,
  placeholder: "Supports markdown!",
  maxHeight: "300px"
});


const $descriptionInput = $('#description')
const $descriptionCard = $('#descriptionCard')
const descriptionMockText = $descriptionCard.text()
const $descriptionCharCounter = $('#descriptionCharCounter')
$descriptionCharCounter.text($descriptionInput.val().length)

const $titleInput = $('#title')
const $titleCard = $('#titleCard')
const titleMockText = $titleCard.text()
const $titleCharCounter = $('#titleCharCounter')
$titleCharCounter.text($titleInput.val().length)

const $tags = $('#tags')
const $tagsCounter = $('#tagsCounter')


$titleInput.on('input', () => {
  const titleText = $titleInput.val()
  const count = titleText.length
  $titleCharCounter.text(count)

  if (count === 0) {
    $titleCard.text(titleMockText)
  }
  else {
    $titleCard.text(titleText)
  }
})

$descriptionInput.on('input', () => {
  const descriptionText = $descriptionInput.val()
  const count = descriptionText.length
  $descriptionCharCounter.text(count)

  if (count === 0) {
    $descriptionCard.text(descriptionMockText)
  } else {
    $descriptionCard.text(descriptionText)
  }
})

$tags.on('input', () => {
  const numTags = $tags.val().replace(/[^#]/g, "").length
  if (numTags <= 5) {
    $tagsCounter.text(numTags)
  }
})
