'use strict';
(function () {
  const elem = {
    success: document.querySelector('#challenge-success'),
    content: document.querySelector('#challenge-content'),
    form: document.querySelector('#challenge-form'),
    info: document.querySelector('#challenge-info'),
    group: document.querySelector('#challenge-answer-group'),
    input: document.querySelector('#challenge-answer'),
    submit: document.querySelector('#challenge-form .btn'),
  };

  const url = new URL(window.location);
  url.protocol = 'wss';
  const webSocket = new WebSocket(url);

  elem.info.innerHTML = 'Lag et svar som tilfredstiller følgene regulære utrykk';

  const current = {
    match: [],
    notmatch: [],
  };

  const updateMarkers = () => {
    for (const [i, rex] of current.match.entries()) {
      const marker = document.querySelector(`#match-${i}`);
      if (rex.test(elem.input.value)) {
        marker.classList.remove('text-error');
        marker.classList.add('text-success');
      } else {
        marker.classList.add('text-error');
        marker.classList.remove('text-success');
      }
    }
    for (const [i, rex] of current.notmatch.entries()) {
      const marker = document.querySelector(`#notmatch-${i}`);
      if (rex.test(elem.input.value)) {
        marker.classList.add('text-error');
        marker.classList.remove('text-success');
      } else {
        marker.classList.remove('text-error');
        marker.classList.add('text-success');
      }
    }
  };

  webSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    switch (data.type) {
      case 'challenge':
        current.match = data.value.match.map(
          ({source, flags}) => new RegExp(source, flags)
        );
        current.notmatch = data.value.notmatch.map(
          ({source, flags}) => new RegExp(source, flags)
        );

        elem.content.innerHTML = []
          .concat(
            current.match.map(
              (x, i) =>
                `<span id="match-${i}"><b>Match:</b> ${x.toString()}</span>`
            )
          )
          .concat(
            current.notmatch.map(
              (x, i) => `<span id="notmatch-${i}"><b>Don't match:</b> ${x.toString()}</span>`
            )
          )
          .join('<br>');
        updateMarkers();
        break;

      case 'success':
        webSocket.close();
        elem.form.remove();
        elem.success.innerHTML = data.value;
        break;

      default:
      case 'error':
        elem.submit.removeAttribute('disabled');
        elem.group.classList.remove('warning');
        elem.group.classList.add('error');
        elem.input.value = '';
        break;
    }
  };

  elem.input.addEventListener('change', updateMarkers);
  elem.input.addEventListener('keyup', updateMarkers);

  elem.form.addEventListener('submit', (event) => {
    event.preventDefault();
    event.stopPropagation();

    elem.group.classList.remove('error');
    elem.group.classList.add('warning');
    elem.submit.setAttribute('disabled', true);
    webSocket.send(JSON.stringify({type: 'response', value: elem.input.value}));

    return false;
  });
})();
