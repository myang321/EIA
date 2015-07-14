/**
 * Created by Steve on 7/14/2015.
 */
(function () {
    var dialog = document.getElementById('window_signup');
    document.getElementById('signup').onclick = function () {
        dialog.show();
    };
    document.getElementById('exit_signup').onclick = function () {
        dialog.close();
    };
})();

(function () {
    var dialog = document.getElementById('window_login');
    document.getElementById('login').onclick = function () {
        dialog.show();
    };
    document.getElementById('exit_login').onclick = function () {
        dialog.close();
    };
})();