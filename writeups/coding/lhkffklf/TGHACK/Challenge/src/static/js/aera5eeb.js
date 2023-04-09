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

  elem.info.innerHTML = 'Musikk i høy velositet';

  webSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    switch (data.type) {
      case 'challenge':
        elem.content?.children?.[0]?.stop();
        elem.content.innerHTML = `
          <midi-player
            src="data:audio/midi;base64,${data.value}"
            sound-font>
          </midi-player>`;
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
