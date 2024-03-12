import { Container, Typography, Box, Button } from '@mui/material';
import  { useEffect, useState } from 'react';

interface AudioFile {
  file: string;
}
const isProduction = import.meta.env.MODE === "production";
const apiRootPath = isProduction ? "" : "/api";

function Index() {
  const [audioFiles, setAudioFiles] = useState<AudioFile[]>([]);
  const [cameraStarted, setCameraStarted] = useState(false);
  useEffect(() => {
    setAudioFiles([{ file: "test.mp3" }]);
    // TODO
    // Fetch audio files from server
    // setAudioFiles(response);
  }, []);

  const playSound = (file: string) => {
    fetch(`/play/${file}`, {
      method: "POST"
    })
    .then(res => console.log(res))
    .catch(() => {
      alert("There was an error with the camera, refreshing might fix this or someone else is looking through the camera");
    });
  };

  return (
    <Container
      maxWidth="xl"
      sx={{ minHeight: "100vh", pl: "0", pr: "0" }}
    >
      <Typography variant="h1">Watch Cam</Typography>
      <Box>
        <img
          alt="Stream Loading..."
          id="live-stream"
          onError={() => alert("There was an error with the camera, refreshing might fix this or someone else is looking through the camera")}
          onLoad={() => setCameraStarted(true)}
          src={`${apiRootPath}/video_feed`}
          style={{ width: '90%', height: 'auto' }}
        />

        {!cameraStarted && <Typography variant="body1">Starting Camera ...</Typography>}

        {audioFiles.length > 0 && false && (
          <Box style={{ display: 'flex', flexDirection: 'column', paddingBottom: '1rem' }}>
            <Typography variant="h2">Sounds To Play:</Typography>
            <Box style={{ flexDirection: 'row' }}>
              {audioFiles.map(({ file }) => (
                <Button key={file} onClick={() => playSound(file)}>{file}</Button>
              ))}
            </Box>
          </Box>
        )}

        <Typography variant="body1"><a style={{ color: 'inherit' }} href="/videos">See Recordings</a></Typography>
      </Box>
    </Container>
  );
}

export default Index;