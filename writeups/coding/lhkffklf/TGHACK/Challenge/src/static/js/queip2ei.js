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

  elem.info.innerHTML = 'Marker endene!';
  elem.content.style.position = 'relative';
  elem.content.style.height = '320px';
  elem.content.style.width = '320px';

  elem.content.addEventListener('click', (event) => {
    event.preventDefault();
    event.stopPropagation();
    if (event.target !== elem.content) {
      const i = event.target.getAttribute('data-id');
      event.target.remove();
      elem.input.value = elem.input.value
        .split(' ')
        .filter(x => x !== i)
        .filter(x => x)
        .join(' ');
      return false;
    }

    const x = event.offsetX - (event.offsetX % 32);
    const y = event.offsetY - (event.offsetY % 32);
    const i = `${x / 32 + 1}x${y / 32 + 1}`;

    elem.input.value = elem.input.value
      .split(' ')
      .concat(i)
      .sort()
      .filter(_x => _x)
      .join(' ');

    const div = document.createElement('div');
    div.setAttribute('data-id', i);
    div.style.background = '#55a';
    div.style.opacity = '0.75';
    div.style.height = '32px';
    div.style.width = '32px';
    div.style.position = 'absolute';
    div.style.left = `${x}px`;
    div.style.top = `${y}px`;
    elem.content.appendChild(div);

    return false;
  });

  webSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    switch (data.type) {
      case 'challenge':
        elem.content.style.background =
          `url(data:image/png;base64,${data.value}) no-repeat center center`;
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
        elem.content.innerHTML = '';
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
