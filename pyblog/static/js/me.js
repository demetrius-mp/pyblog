const $bio = $('#bio')
const $biocharCounter = $('#bioCharCounter')
const $cardBio = $('#cardBio')
$biocharCounter.text($bio.text().trim().length)

$bio.on('input', () => {
  const bio = $bio.val()
  const numCharacters = bio.length
  $biocharCounter.text(numCharacters)
  $cardBio.text(bio)
})