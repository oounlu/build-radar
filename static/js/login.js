// Initialize Firebase
firebase.initializeApp(firebaseConfig);

function googleLogin() {
  var provider = new firebase.auth.GoogleAuthProvider();
  firebase.auth().signInWithPopup(provider).then(function(result) {
    result.user.getIdToken().then(function(idToken) {
      var form = document.createElement('form');
      form.setAttribute('method', 'POST');
      form.setAttribute('action', '/token-signin');
      var hiddenField = document.createElement('input');
      hiddenField.setAttribute('type', 'hidden');
      hiddenField.setAttribute('name', 'idToken');
      hiddenField.setAttribute('value', idToken);
      form.appendChild(hiddenField);
      document.body.appendChild(form);
      form.submit();
    });
  }).catch(function(error) {
      console.error(error);
  });
}

function githubLogin() {
  var provider = new firebase.auth.GithubAuthProvider();
  firebase.auth().signInWithPopup(provider).then(function(result) {
    result.user.getIdToken().then(function(idToken) {
      var form = document.createElement('form');
      form.setAttribute('method', 'POST');
      form.setAttribute('action', '/token-signin');
      var hiddenField = document.createElement('input');
      hiddenField.setAttribute('type', 'hidden');
      hiddenField.setAttribute('name', 'idToken');
      hiddenField.setAttribute('value', idToken);
      form.appendChild(hiddenField);
      document.body.appendChild(form);
      form.submit();
    });
  }).catch(function(error) {
      console.error(error);
  });
}