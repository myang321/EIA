/**
 * Created by Steve on 7/14/2015.
 */
/**
 * Created by Steve on 7/14/2015.
 */
(function () {
    var dialog = document.getElementById('window_signup');
    //var dialog = $("#window_signup");
    document.getElementById('signup').onclick = function () {
        dialog.show();
        //$("#window_login").dialog('close');
        document.getElementById('window_login').close();
    };
    document.getElementById('exit_signup').onclick = function () {
        dialog.close();
    };
})();

(function () {
    var dialog = document.getElementById('window_login');
    //var dialog = $("#window_login");
    document.getElementById('login').onclick = function () {
        dialog.show();
        //$("#window_signup").dialog('close');
        document.getElementById('window_signup').close();
    };
    document.getElementById('exit_login').onclick = function () {
        dialog.close();
    };
})();