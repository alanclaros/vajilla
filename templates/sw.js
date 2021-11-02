const host_open = "https://ntsoft-bolivia.com/teamwork";
const webpush_icon = "https://ntsoft-bolivia.com/webpush_image.png";
const webpush_badge = 'https://ntsoft-bolivia.com/cel_notificacion002_128.png';
const action_ver_icon = "https://ntsoft-bolivia.com/webpush_image.png";
const action_eliminar_icon = "https://ntsoft-bolivia.com/webpush_action_eliminar.png";

self.addEventListener('push', function (event) {
    // Retrieve the textual payload from event.data (a PushMessageData object).
    // Other formats are supported (ArrayBuffer, Blob, JSON), check out the documentation
    // on https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData.
    const eventInfo = event.data.text();
    const data = JSON.parse(eventInfo);
    const head = data.head || 'New Notification';
    const body = data.body || 'This is default content. Your notification didnt have one';

    // Keep the service worker alive until the notification is created.
    event.waitUntil(
        self.registration.showNotification(head, {
            body: body,
            //icon: 'https://i.imgur.com/MZM3K5w.png'
            icon: webpush_icon,
            badge: webpush_badge,
            //dir: 'rtl',
            actions: [
                {
                    action: 'accion-ver',
                    title: 'Ver-Web',
                    icon: action_ver_icon
                },
                {
                    action: 'accion-eliminar',
                    title: 'Borrar',
                    icon: action_eliminar_icon
                }
            ],
            vibrate: [500, 110, 500, 110, 450, 110, 200, 110, 170, 40, 450, 110, 200, 110, 170, 40, 500],
            //sound: 'https://gidaesrl.com/webpush_alert.mp3',
        })

    );

    //const promiseChain = clients.openWindow("https://gidaesrl.com");
    //event.waitUntil(promiseChain);
    //image: 'https://gidaesrl.com/cabecera002.jpg',
    //acc, 20210124, anterior badge: 'https://gidaesrl.com/prueba001_128.png',
});

self.addEventListener('notificationclick', function (event) {
    console.log('On notification click: ', event.notification.tag);
    // Android doesn't close the notification when you click on it
    // See: http://crbug.com/463146

    //para cerrar la notificacion al hacer click en la notificacion
    //event.notification.close();

    //abrir una url al hacer click en la notificacion
    //const promiseChain = clients.openWindow("https://gidaesrl.com");
    //event.waitUntil(promiseChain);

    //segun las accion dedicimos que hacer
    if (!event.action) {
        // Was a normal notification click
        //console.log('Notification Click.');
        return;
    }

    switch (event.action) {
        case 'accion-ver':
            //console.log('click en accion ver.');
            const promiseChain = clients.openWindow(host_open);
            event.waitUntil(promiseChain);

            break;

        case 'accion-eliminar':
            //console.log('click accion eliminar.');
            event.notification.close();

            break;

        default:
            //console.log('no se reconoce la accion');
            break;
    }
});


/*// Register event listener for the 'push' event.
self.addEventListener('push', function (event) {
    // Retrieve the textual payload from event.data (a PushMessageData object).
    // Other formats are supported (ArrayBuffer, Blob, JSON), check out the documentation
    // on https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData.
    const eventInfo = event.data.text();
    const data = JSON.parse(eventInfo);
    const head = data.head || 'New Notification';
    const body = data.body || 'This is default content. Your notification didnt have one';

    // Keep the service worker alive until the notification is created.
    event.waitUntil(
        self.registration.showNotification(head, {
            body: body,
            //icon: 'https://i.imgur.com/MZM3K5w.png'
            icon: 'https://gidaesrl.com/webpush_image.png',
            badge: 'https://gidaesrl.com/cel_notificacion002_128.png',
            actions: [
                {
                    action: 'ver-action',
                    title: 'Ver Notificacion',
                    icon: 'https://gidaesrl.com/webpush_action_ver.png'
                },
                {
                    action: 'eliminar-action',
                    title: 'Eliminar',
                    icon: 'https://gidaesrl.com/webpush_action_eliminar.png'
                }
            ],
            //vibrate: [500, 110, 500, 110, 450, 110, 200, 110, 170, 40, 450, 110, 200, 110, 170, 40, 500],
            //sound: 'https://gidaesrl.com/webpush_alert.mp3',
        })

    );
    //image: 'https://gidaesrl.com/cabecera002.jpg',
    //acc, 20210124, anterior badge: 'https://gidaesrl.com/prueba001_128.png',
});*/