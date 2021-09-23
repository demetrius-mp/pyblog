toastr.options = {
  "closeButton": false,
  "debug": false,
  "newestOnTop": true,
  "progressBar": true,
  "positionClass": "toast-bottom-right",
  "preventDuplicates": false,
  "onclick": null,
  "showDuration": "300",
  "hideDuration": "1000",
  "timeOut": "3000",
  "extendedTimeOut": "1000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
}
function showToast(category, message){
  switch (category) {
    case 'success':
      toastr.success(message)
      break
    case 'warning':
      toastr.warning(message)
      break
    case 'info':
      toastr.info(message)
      break
    case 'error':
      toastr.error(message)
      break
  }
}