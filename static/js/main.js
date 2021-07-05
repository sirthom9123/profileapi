const form = document.getElementById('profile-form')
const gender = document.getElementById('gender')
const title = document.getElementById('title')
const firstName = document.getElementById('first_name')
const lastName = document.getElementById('last_name')
const dob = document.getElementById('dob')
const age = document.getElementById('age')
const phone = document.getElementById('phone')
const cell = document.getElementById('cell')
const alertBox = document.getElementById('alert-box')
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

const handleAlerts = (type, msg) => {
  alertBox.innerHTML = `
    <div class="alert alert-${type}" role="alert">
        ${msg}
    </div>
    `
}

form.addEventListener('submit', (e) => {
  e.preventDefault()

  const formData = new FormData()
  formData.append('csrfmiddlewaretoken', csrf)
  formData.append('gender', gender.value)
  formData.append('title', title.value)
  formData.append('first_name', firstName.value)
  formData.append('last_name', lastName.value)
  formData.append('dob', dob.value)
  formData.append('age', age.value)
  formData.append('phone', phone.value)
  formData.append('cell', cell.value)

  $.ajax({
    type: 'POST',
    url: '/profile_form/',
    data: formData,
    success: function (response) {
      handleAlerts('success', 'Profile created successfully.')
      form.reset()
    },
    error: function (error) {
      handleAlerts('danger', 'Ooops... something went wrong!')
    },
    processData: false,
    contentType: false,
  })
})
