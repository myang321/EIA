/**
 * Created by Steve on 7/14/2015.
 */
(function () {
    var dialog = document.getElementById('window_signup');
    document.getElementById('signup').onclick = function () {
        dialog.show();
        $("#welcome1").hide();
        $("#welcome2").hide();
    };
    document.getElementById('exit_signup').onclick = function () {
        dialog.close();
        $("#welcome1").show();
        $("#welcome2").show();
    };
})();

(function () {
    var dialog = document.getElementById('window_login');
    document.getElementById('login').onclick = function () {
        dialog.show();
        $("#welcome1").hide();
        $("#welcome2").hide();
    };
    document.getElementById('exit_login').onclick = function () {
        dialog.close();
        $("#welcome1").show();
        $("#welcome2").show();
    };
})();