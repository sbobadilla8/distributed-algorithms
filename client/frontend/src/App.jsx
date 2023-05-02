import { useState, useEffect } from "react";
import axios from "axios";
import {
  AbsoluteCenter,
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  useToast,
} from "@chakra-ui/react";

import LocalFiles from "./components/LocalFiles.jsx";
import ExternalFiles from "./components/ExternalFiles.jsx";

function App() {
  const toast = useToast();
  const [backendAddress, setBackendAddress] = useState("");
  const [serverAddress, setServerAddress] = useState("");
  const [connected, setConnected] = useState(null);

  const checkAddress = async () => {
    try {
      const backendResponse = await axios.post(
        `http://${backendAddress}/check`
      );
      const serverResponse = await axios.post(`http://${serverAddress}/check`);
      if (backendResponse.status === 204 && serverResponse.status === 204) {
        setConnected(true);
      } else {
        toast({
          title: "Error",
          description: "Couldn't connect. Please try again.",
          status: "error",
          duration: 3000,
          isClosable: true,
        });
      }
    } catch (e) {
      toast({
        title: "Error",
        description: "Something went wrong.",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  };

  return (
    <>
      {connected === null ? (
        <Box h="100vh">
          <AbsoluteCenter p="4" axis="both">
            <FormControl>
              <FormLabel>Enter the backend address:</FormLabel>
              <Input
                type="text"
                value={backendAddress}
                onChange={(e) => setBackendAddress(e.target.value)}
              />
            </FormControl>
            <FormControl>
              <FormLabel>Enter the index server address:</FormLabel>
              <Input
                type="text"
                value={serverAddress}
                onChange={(e) => setServerAddress(e.target.value)}
              />
            </FormControl>
            <Button colorScheme="teal" m={4} w="80%" onClick={checkAddress}>
              Accept
            </Button>
          </AbsoluteCenter>
        </Box>
      ) : (
        <Box m={4}>
          <LocalFiles
            backendAddress={backendAddress}
            serverAddress={serverAddress}
          />
          <ExternalFiles
            serverAddress={serverAddress}
            backendAddress={backendAddress}
          />
        </Box>
      )}
    </>
  );
}

export default App;
