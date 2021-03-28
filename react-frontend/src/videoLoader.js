async function videoLoader() {
    const request = await fetch('/getPickle');
    const response = await request.json()
    const videos = response['video']['videoPaths']
    const videoPaths = []
    videos.map((item) => {
        videoPaths.append({'path':item['videoPathForReact']})
    })
    return videoPaths
  }

  export default videoLoader