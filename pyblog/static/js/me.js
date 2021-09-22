const $bio = $('#bio')
const $biocharCounter = $('#bioCharCounter')
const $cardBio = $('#cardBio')

const $editableLearning = $('#editableCurrentlyLearning')
const $inputLearning = $('#currently_learning')

const $editableExperience = $('#editableExperienceIn')
const $inputExperience = $('#experience_in')

const $editableLooking = $('#editableLookingTo')
const $inputLooking = $('#looking_to')

$biocharCounter.text($bio.text().trim().length)

$bio.on('input', () => {
  const bio = $bio.val()
  const numCharacters = bio.length
  $biocharCounter.text(numCharacters)
  $cardBio.text(bio)
})

$editableLearning.on('input', () => {
  const learning = $editableLearning.text().trim()
  $inputLearning.val(learning)
})

$editableExperience.on('input', () => {
  const experience = $editableExperience.text().trim()
  $inputExperience.val(experience)
})

$editableLooking.on('input', () => {
  const looking = $editableLooking.text().trim()
  $inputLooking.val(looking)
})