import { useState } from "react";
import axios from "axios";
import {
  Button,
  Card,
  CardBody,
  CardHeader,
  Flex,
  Heading,
  Input,
  Stack,
  StackDivider,
  useToast,
} from "@chakra-ui/react";

import FileCard from "./FileCard.jsx";

const ExternalFiles = ({ serverAddress, backendAddress }) => {
  const toast = useToast();

  const [input, setInput] = useState("");
  const [results, setResults] = useState([]);

  const searchFile = async () => {
    try {
      const { data } = await axios.get(
        `http://${serverAddress}/file?input=${input}`
      );
      setResults(data.map((item) => ({ ...item, progress: 0, status: "" })));
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
      <Flex direction="row" justify="center">
        <Heading size="lg">Search for a file</Heading>
      </Flex>
      <Flex direction="row" align="center" gap={4} m={4}>
        <Input
          placeholder="File name"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <Button
          type="button"
          colorScheme="teal"
          isLoading={false}
          onClick={searchFile}
        >
          Search
        </Button>
      </Flex>
      <Card>
        <CardHeader>
          <Heading size="md">Search results</Heading>
        </CardHeader>

        <CardBody>
          <Stack divider={<StackDivider />} spacing="4">
            {results.map((item) => (
              <FileCard
                key={item.filename}
                item={item}
                setResults={setResults}
                backendAddress={backendAddress}
              />
            ))}
          </Stack>
        </CardBody>
      </Card>
    </>
  );
};

export default ExternalFiles;
