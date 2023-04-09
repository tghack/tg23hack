'use strict';

const fs = require('node:fs/promises');
const cp = require('node:child_process');
const App = require('nnn');
const util = require('node:util');
const {PNG} = require('pngjs');
const crypto = require('node:crypto');
const syspath = require('node:path');
const makeMidi = require('./make-midi');
const {WebSocketServer} = require('ws');

const ejs = util.promisify(require('ejs').renderFile);
const execFile = util.promisify(cp.execFile);

class Ctx {
  constructor(req, res) {
    this.req = req;
    this.res = res;
  }

  async render(template, locals = {}) {
    const opts = {localsName: 'self', _with: false};
    if (this.user) locals.user = this.user;
    locals.content = await ejs(`./templates/${template}`, locals, opts);
    const html = await ejs('./templates/skeleton.html', locals, opts);
    return html;
  }

  async serve(path) {
    const parent = syspath.join(__dirname, 'static');
    const child = syspath.join(__dirname, 'static', path);

    const relative = syspath.relative(parent, child);
    if (!relative || relative.startsWith('..') || syspath.isAbsolute(relative))
      return this.throw(404);

    try {
      const data = await fs.readFile(child);
      return this.res.end(data);
    } catch (err) {
      if (err.code === 'ENOENT') return this.throw(404);
      throw err;
    }
  }

  throw(code) {
    throw new App.HttpError(code);
  }
}

const app = new App({context: Ctx, trim: true, case: true});

app.use(async function (next) {
  const t = new Date();
  // eslint-disable-next-line callback-return
  await next();
  console.log(
    `${this.req.connection.remoteAddress} ${this.req.method} ${this.req.url} ` +
      `${this.res.statusCode} (${new Date() - t} ms)`
  );
});
app.use(async function (next) {
  this.payload = '';
  await new Promise((resolve, reject) => {
    this.req.on('data', (chunk) => {
      this.payload += chunk;
    });
    this.req.on('error', reject);
    this.req.on('end', resolve);
  });
  // eslint-disable-next-line callback-return
  await next();
});

app.catch.on('400', async function () {
  this.res.statusCode = 400;
  this.res.end();
});
app.catch.on('403', async function () {
  this.res.statusCode = 403;
  this.res.end();
});
app.catch.on('404', async function () {
  this.res.statusCode = 404;
  this.res.end();
});
app.catch.on('500', async function (err) {
  if (err) console.log(err);
  this.res.statusCode = 500;
  this.res.end();
});

app.get('/', async function () {
  this.res.setHeader('location', '/1');
  this.res.statusCode = 302;
  this.res.end();
});

app.get('/static/**', async function (path) {
  return this.serve(path);
});

const challenges = {sockets: {}, count: 0};
const defineChallange = (js, loop, run, flag) => {
  challenges.count += 1;
  const active = challenges.count;

  const pathname = `/${active}`;
  app.get(pathname, async function () {
    const html = await this.render('challenge.html', {
      active,
      js,
      count: challenges.count,
    });
    this.res.setHeader('content-type', 'text/html');
    this.res.end(html);
  });

  let challenge = null;
  let previous = null;

  const connections = new Set();
  const wss = new WebSocketServer({noServer: true});
  challenges.sockets[pathname] = wss;

  wss.on('connection', (ws) => {
    connections.add(ws);

    ws.on('error', (err) => console.log(err));

    ws.on('message', (data) => {
      let message = null;
      try {
        message = JSON.parse(data);
      } catch (err) {
        // meh
      }

      if (!message || message.type !== 'response')
        return ws.send(JSON.stringify({type: 'error'}));

      if (typeof message.value !== 'string')
        return ws.send(JSON.stringify({type: 'error'}));

      if (message.value !== challenge && message.value !== previous)
        return ws.send(JSON.stringify({type: 'error'}));

      ws.send(
        JSON.stringify({
          type: 'success',
          value: `
            <h2 class="text-center">👏</h2>
            <p class="text-center">
              ${flag}
            </p>
          `,
        })
      );
    });

    ws.on('close', () => {
      connections.delete(ws);
      console.log(`${ws._socket.remoteAddress} DISCONNECT ${pathname}`);
    });

    console.log(`${ws._socket.remoteAddress} CONNECT ${pathname}`);
  });

  setInterval(async () => {
    const {result, value} = await run();

    previous = challenge;
    challenge = String(result);

    wss.clients.forEach((client) => {
      const data = JSON.stringify({type: 'challenge', value});
      client.send(data);
    });
    previous = null;
  }, loop);
};

defineChallange('iequae6u', 2000, async () => {
  const a = crypto.randomInt(10, 50);
  const b = crypto.randomInt(2, 10);
  const c = crypto.randomInt(5, 10);
  const d = crypto.randomInt(2, 5);
  const value = `${a * b} / ${b} + ${c}^${d}`;
  const result = a + c ** d;
  return {result, value};
}, 'TG23{mennesker_er_ikke_gode_i_hoderegning}');

defineChallange('eij4eej6', 2000, async () => {
  const a = crypto.randomInt(10, 50);
  const b = crypto.randomInt(2, 10);
  const c = crypto.randomInt(5, 10);
  const d = crypto.randomInt(2, 5);

  const value = `${a * b} / ${b} + ${c}^${d}`;
  const result = a + c ** d;

  const {stdout} = await execFile(
    '/usr/bin/convert',
    ['-pointsize', '14', `label:${value}`, 'png:-'],
    {encoding: 'buffer'}
  );

  return {result, value: stdout.toString('base64')};
}, 'TG23{bare_i_tilfellet_mennesker_kan_lese_utf8}');

defineChallange('uw8fie6a', 5000, async () => {
  const result = crypto.randomUUID();
  const {stdout} = await execFile(
    '/usr/bin/qrencode',
    ['-o-', result],
    {encoding: 'buffer'}
  );
  const value = stdout.toString('base64');
  return {result, value};
}, 'TG23{mennesker_kan_hvertfall_ikke_lese_qr_koder}');

defineChallange('oocho7au', 5000, async () => {
  const png = new PNG({width: 100, height: 100, filterType: -1});
  let result = 0;

  const ratio = Math.random() * 0.3 + 0.05;
  for (let y = 0; y < png.height; y += 1) {
    for (let x = 0; x < png.width; x += 1) {
      // eslint-disable-next-line no-bitwise
      const i = (png.width * y + x) << 2;
      let r, g, b;

      if (Math.random() < ratio) {
        r = 0xff;
        g = 0xd7;
        b = 0x00;
        result += 1;
      } else {
        r = Math.floor(Math.random() * 256);
        g = Math.floor(Math.random() * 256);
        b = Math.floor(Math.random() * 256);
        if (r === 0xff && g === 0xd7 && b === 0x00) {
          result += 1;
        }
      }

      png.data[i + 0] = r;
      png.data[i + 1] = g;
      png.data[i + 2] = b;
      png.data[i + 3] = 0xff;
    }
  }

  const img = PNG.sync.write(png);

  return {result: String(result), value: img.toString('base64')};
}, 'TG23{menneskers_øyne_har_en_dpi_på_170_så_dette_burde_være_umulig}');

defineChallange('aera5eeb', 10000, async () => {
  const result = crypto.randomUUID();
  const value = makeMidi(result);
  return {result, value};
}, 'TG23{mennesker_har_heller_ikke_god_hørrsel}');

defineChallange('queip2ei', 5000, async () => {
  const result = [];

  const columns = [];
  for (let y = 1; y <= 10; y += 1) {
    const row = [];
    for (let x = 1; x <= 10; x += 1) {
      const d = ['dd', 'dt'][crypto.randomInt(0, 2)];
      const n = crypto.randomInt(1, 7);
      if (d === 'dd') result.push(`${x}x${y}`);
      row.push(syspath.join(__dirname, 'assets', `${d}${n}.png`));
    }
    columns.push(`<(convert +append ${row.join(' ')} png:-)`);
  }
  const cmd = `convert -append ${columns.join(' ')} png:-`;

  const {stdout} = await execFile(
    '/bin/sh',
    ['-c', cmd],
    {encoding: 'buffer'}
  );

  return {result: result.sort().join(' '), value: stdout.toString('base64')};
}, 'TG23{hvor_god_er_menneskers_donald_klassifiserings_algoritme}');

defineChallange('eivai2Ei', 2000, async () => {
  const result = []
    .concat(Array
      .from('abcdefghijklmnopqrstuvwxyz')
      .sort(() => Math.random() - 0.5)
      .slice(0, 5))
    .concat(Array
      .from('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
      .sort(() => Math.random() - 0.5)
      .slice(0, 5))
    .sort(() => Math.random() - 0.5)
    .join('');

  const value = {match: [], notmatch: []};

  const caser = (c) => c.toUpperCase() === c ? '[A-Z]' : '[a-z]';
  switch (Math.floor(Math.random() * 3)) {
    case 0:
      value.match.push({source: `${result[0]}.${result[2]}`, flags: ''});
      value.match.push({source: `${result[1]}.*${result[4]}`, flags: ''});
      value.match.push({source: `${result[3]}.${result[5]}`, flags: ''});
      value.match.push({source: `${result[4]}.*${result[7]}`, flags: ''});
      value.match.push({source: `${result[6]}..${result[9]}`, flags: ''});
      value.match.push({source: `${caser(result[6])}${caser(result[7])}${result[8]}`, flags: ''});
      value.notmatch.push({source: `${result[3]}.*${result[2]}`, flags: ''});
      value.notmatch.push({source: `${result[6]}.*${result[5]}`, flags: ''});
      value.notmatch.push({source: `${result[8]}.*${result[7]}`, flags: ''});
      value.match.sort(() => Math.random() - 0.5);
      value.notmatch.sort(() => Math.random() - 0.5);
      value.match.unshift({source: `^[a-z]{${result.length}}$`, flags: 'i'});
      break;

    case 1:
      value.match.push({source: `${result[0]}.${result[2]}`, flags: ''});
      value.match.push({source: `${result[1]}.*${result[4]}`, flags: ''});
      value.match.push({source: `${result[3]}.${result[5]}`, flags: ''});
      value.match.push({source: `${result[4]}.*${result[7]}`, flags: ''});
      value.match.push({source: `${result[6]}.${result[8]}`, flags: ''});
      value.match.push({source: `${caser(result[7])}${caser(result[8])}${result[9]}`, flags: ''});
      value.notmatch.push({source: `${result[3]}.*${result[2]}`, flags: ''});
      value.notmatch.push({source: `${result[6]}.*${result[5]}`, flags: ''});
      value.notmatch.push({source: `${result[9]}.*${result[8]}`, flags: ''});
      value.match.sort(() => Math.random() - 0.5);
      value.notmatch.sort(() => Math.random() - 0.5);
      value.match.unshift({source: `^[a-z]{${result.length}}$`, flags: 'i'});
      break;

    default:
    case 2:
      value.match.push({source: `${result[0]}..${result[3]}`, flags: ''});
      value.match.push({source: `${result[2]}.*${result[4]}`, flags: ''});
      value.match.push({source: `${result[3]}.+${result[5]}`, flags: ''});
      value.match.push({source: `${result[6]}.+${result[9]}`, flags: ''});
      value.match.push({source: `${result[7]}.*${result[8]}`, flags: ''});
      value.match.push({source: `${result[1]}${caser(result[2])}${caser(result[3])}${result[4]}`, flags: ''});
      value.notmatch.push({source: `${result[9]}.*${result[8]}`, flags: ''});
      value.notmatch.push({source: `${result[7]}.*[${result[6]}${result[5]}]`, flags: ''});
      value.notmatch.push({source: `${result[6]}.*${result[5]}|${result[1]}.*${result[0]}`, flags: ''});
      value.notmatch.push({source: `${result[4]}.*${result[3]}`, flags: ''});
      value.match.sort(() => Math.random() - 0.5);
      value.notmatch.sort(() => Math.random() - 0.5);
      value.match.unshift({source: `^[a-z]{${result.length}}$`, flags: 'i'});
      break;
  }

  return {result, value};
}, 'TG23{hold_deg_unna_jeg_kan_regulære_utrykk}');

app
  .start({http: Number.parseInt(process.env.SERVER_PORT, 10) || 80})
  .then(() => {
    console.log(`server listening on port: ${app.httpServer.address().port}`);
  });

app.httpServer.on('upgrade', (req, soc, head) => {
  try {
    const {pathname} = new URL(req.url, 'http://localhost/');
    if (Object.hasOwn(challenges.sockets, pathname)) {
      challenges.sockets[pathname].handleUpgrade(req, soc, head, (ws) => {
        challenges.sockets[pathname].emit('connection', ws, req);
      });
    } else {
      soc.destroy();
    }
  } catch (err) {
    console.log(err);
    soc.destroy();
  }
});
