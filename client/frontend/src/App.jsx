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

function App({ serverAddress, backendAddress }) {
  const toast = useToast();

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
    </>
  );
}

export default App;
