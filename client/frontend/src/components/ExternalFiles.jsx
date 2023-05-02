import { useState } from "react";
import axios from "axios";
import {
  Box,
  Button,
  Card,
  CardBody,
  CardHeader,
  FormControl,
  FormLabel,
  Heading,
  IconButton,
  Input,
  Progress,
  Stack,
  StackDivider,
  Stat,
  StatGroup,
  StatLabel,
  StatNumber,
  useToast,
} from "@chakra-ui/react";
import { BsDownload } from "react-icons/bs";
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
      setResults(data.map((item) => ({ ...item, progress: 0 })));
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
      <FormControl>
        <FormLabel>Search for a file</FormLabel>
        <Input
          placeholder="File name"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
      </FormControl>
      <Button
        type="button"
        mt={4}
        colorScheme="teal"
        isLoading={false}
        onClick={searchFile}
      >
        Search
      </Button>
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
