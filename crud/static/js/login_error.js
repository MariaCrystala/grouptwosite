document.addEventListener('DOMContent Loaded', function(){
    const hasError = window.location.search.includes('error')||
                     document. querySelector('[data-django-message]')?.textContent.includes('Invalid');

    if (hasError) {
        const usernameInput = document.getElementByid('username');
        const passwordInput = document.getElementByid('password');
        const loginError = document.getElementByid('loginError');

        usernameInput.style.borderColor = '#ef4444';
        passwordInput.style.borderColor = '#eff444';
        loginError.classList.remove('hidden');

        function clearError(){
            usernameInput.style.borderColor ='';
            passswordInput.style.bordercolor='';
            loginError.classList.add('hidden');
        }
        usernameInput.addEventListener('input', clearError);
        passwordInput.addEventListener('input', clearError);
    }
});