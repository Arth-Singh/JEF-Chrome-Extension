const NATIVE_HOST_NAME = 'com.odin.jef_tester';

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'runTest') {
        runJEFTest(request.test, request.text)
            .then(result => {
                sendResponse({ success: true, result: result });
            })
            .catch(error => {
                sendResponse({ success: false, error: error.message });
            });
        return true;
    }
});

async function runJEFTest(testType, text) {
    return new Promise((resolve, reject) => {
        const port = chrome.runtime.connectNative(NATIVE_HOST_NAME);
        
        let responseReceived = false;
        
        port.onMessage.addListener((response) => {
            responseReceived = true;
            if (response.error) {
                reject(new Error(response.error));
            } else {
                resolve(response.result);
            }
            port.disconnect();
        });
        
        port.onDisconnect.addListener(() => {
            if (!responseReceived) {
                const error = chrome.runtime.lastError;
                reject(new Error(error ? error.message : 'Native messaging host disconnected'));
            }
        });
        
        port.postMessage({
            command: testType,
            text: text
        });
    });
}