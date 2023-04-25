import { useState, useEffect } from "react";
import axios from "axios";
import {
  Box,
  Input,
  FormControl,
  FormLabel,
  Button,
  Card,
  CardHeader,
  Heading,
  CardBody,
  Stack,
  StackDivider,
  Stat,
  StatLabel,
  StatNumber,
  useToast,
  StatGroup,
  Th,
  TableContainer,
  Table,
  Thead,
  Tr,
  Tbody,
  Td,
  Text,
  Flex,
  IconButton,
} from "@chakra-ui/react";
import { BsDownload } from "react-icons/bs";

function App() {
  const toast = useToast();

  const [input, setInput] = useState("");
  const [results, setResults] = useState([]);
  const [file, setFile] = useState("");
  const [files, setFiles] = useState([]);

  const searchFile = async () => {
    try {
      const { data } = await axios.get(
        "http://localhost:8000/file?input=" + input
      );
      console.log(data);
      setResults(data);
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

  const submitFile = async () => {
    try {
      // Notify Idx Server
      const srvResponse = await axios.post("http://localhost:8000/file", {
        filename: file.name,
        ip: "localhost:8080",
        size: file.size,
        blocks: 5,
        checksum: "asdfqwerzxcv",
      });
      // Notify own backend
      const { data } = await axios.post("http://localhost:8080/files", {
        filename: file.name,
        size: file.size,
        blocks: 5,
      });
      setFiles(data);
    } catch (e) {
      console.log(e);
      toast({
        title: "Error",
        description: "",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const getFiles = async () => {
    try {
      const { data } = await axios.get("http://localhost:8080/files");
      setFiles(data);
    } catch (e) {
      toast({
        title: "Error",
        description: "",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  };

  useEffect(() => {
    getFiles();
  }, []);

  return (
    <>
      <Box m={4}>
        <Heading size="lg">Files being shared</Heading>
        <Flex direction="row" justify="flex-start" align="center">
          <FormControl width="min-content" m={2}>
            <Input
              as="input"
              sx={{
                opacity: 0,
                width: "0.1px",
                height: "0.1px",
                position: "absolute",
              }}
              type="file"
              onChange={(e) => {
                setFile(e.target.files[0]);
              }}
              id="file-input"
            />
            <Button as={FormLabel} colorScheme="teal" htmlFor="file-input">
              Select file
            </Button>
          </FormControl>
          <Text fontSize="xl">{file.name}</Text>
        </Flex>
        <Button type="button" mt={4} colorScheme="teal" onClick={submitFile}>
          Share
        </Button>

        <TableContainer>
          <Table size="sm" variant="striped">
            <Thead>
              <Tr>
                <Th>File</Th>
                <Th>Size</Th>
                <Th>Blocks</Th>
              </Tr>
            </Thead>
            <Tbody>
              {files.map((item, idx) => (
                <Tr key={`file-${idx}`}>
                  <Td>{item.filename}</Td>
                  <Td>{item.size}</Td>
                  <Td>{item.blocks}</Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        </TableContainer>
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
              {results.map((item, idx) => (
                <Box key={`result-${idx}`}>
                  <Heading size="md" textTransform="uppercase">
                    {item.filename}
                  </Heading>
                  <StatGroup>
                    <Stat>
                      <StatLabel>Clients sharing</StatLabel>
                      <StatNumber>{item.clients.length}</StatNumber>
                    </Stat>
                    <Stat>
                      <StatLabel>Size</StatLabel>
                      <StatNumber>{item.size}</StatNumber>
                    </Stat>
                    <Stat>
                      <StatLabel>Number of blocks</StatLabel>
                      <StatNumber>{item.blocks}</StatNumber>
                    </Stat>
                    <IconButton
                      aria-label="download"
                      colorScheme="teal"
                      size="lg"
                      icon={<BsDownload />}
                    />
                  </StatGroup>
                </Box>
              ))}
            </Stack>
          </CardBody>
        </Card>
      </Box>
    </>
  );
}

export default App;
