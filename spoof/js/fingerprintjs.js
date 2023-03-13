// create a fingerprint js account to get an API Key
// https://dashboard.fingerprint.com/signup
// Initialize the agent at application startup.
const fpPromise = import('https://fpjscdn.net/v3/<API Key>')
  .then(FingerprintJS => FingerprintJS.load())

// Get the visitor identifier when you need it.
fpPromise
  .then(fp => fp.get())
  .then(result => {
    // This is the visitor identifier:
    const visitorId = result.visitorId
    console.log(visitorId)
  })