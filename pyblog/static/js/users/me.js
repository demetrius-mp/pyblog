const $cardBio = $('#cardBio')
const $bio = $('#bio')
const $biocharCounter = $('#bioCharCounter')
$biocharCounter.text($bio.val().trim().length)
$bio.on('input', () => {
  const text = $bio.val()
  const numCharacters = text.length
  $biocharCounter.text(numCharacters)
  $cardBio.text(text)
})

const $fullName = $('#full_name')
const $fullNameCounter = $('#fullNameCharCounter')
$fullNameCounter.text($fullName.val().trim().length)
$fullName.on('input', () => {
  const text = $fullName.val()
  const numCharacters = text.length
  $fullNameCounter.text(numCharacters)
})

const $username = $('#username')
const $usernameCounter = $('#usernameCharCounter')
$usernameCounter.text($username.val().trim().length)
$username.on('input', () => {
  const text = $username.val()
  const numCharacters = text.length
  $usernameCounter.text(numCharacters)
})

const $editableLearning = $('#editableCurrentlyLearning')
const $inputLearning = $('#currently_learning')
$editableLearning.on('input', () => {
  const learning = $editableLearning.text().trim()
  $inputLearning.val(learning)
})

const $editableExperience = $('#editableExperienceIn')
const $inputExperience = $('#experience_in')
$editableExperience.on('input', () => {
  const experience = $editableExperience.text().trim()
  $inputExperience.val(experience)
})

const $editableLooking = $('#editableLookingTo')
const $inputLooking = $('#looking_to')
$editableLooking.on('input', () => {
  const looking = $editableLooking.text().trim()
  $inputLooking.val(looking)
})

const $profileCard = $('#profileCard')
$profileCard.on('click', '.editable', (e) => {
  $(e.target).attr('contenteditable','true')
  $(e.target).focus()
})
$profileCard.on('blur', '.editable', (e) => {
  $(e.target).attr('contenteditable','false')
})
