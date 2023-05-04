import { Box, Card, CardBody } from "@chakra-ui/react";

import LocalFiles from "./components/LocalFiles.jsx";
import ExternalFiles from "./components/ExternalFiles.jsx";

function App({ serverAddress, backendAddress }) {
  return (
    <>
      <Box m={4}>
        <Card variant="outline" m={4}>
          <CardBody>
            <LocalFiles
              backendAddress={backendAddress}
              serverAddress={serverAddress}
            />
          </CardBody>
        </Card>
        <Card variant="outline" m={4} p={4}>
          <ExternalFiles
            serverAddress={serverAddress}
            backendAddress={backendAddress}
          />
        </Card>
      </Box>
    </>
  );
}

export default App;
