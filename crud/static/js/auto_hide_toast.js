document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        const errorToast = document.getElementById('toast-error');
        if (errorToast) errorToast.style.display = 'none';
        const successToast = document.getElementById('toast-success');
        if (successToast) successToast.style.display = 'none';
    }, 3000);
});