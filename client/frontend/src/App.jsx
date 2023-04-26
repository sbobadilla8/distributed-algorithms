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
  useDisclosure,
} from "@chakra-ui/react";
import { BsDownload } from "react-icons/bs";
import FilePicker from "./components/FilePicker.jsx";

function App() {
  const toast = useToast();

  const { isOpen, onOpen, onClose } = useDisclosure();

  const [input, setInput] = useState("");
  const [results, setResults] = useState([]);

  const [files, setFiles] = useState([]);

  const searchFile = async () => {
    try {
      const { data } = await axios.get(
        "http://localhost:8000/file?input=" + input
      );
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

  const submitFile = async (file) => {
    try {
      const { data } = await axios.post("http://localhost:8080/files", {
        file,
      });
      setFiles(data);
      onClose();
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
          <Button colorScheme="teal" onClick={onOpen}>
            Select file
          </Button>
        </Flex>

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
      <FilePicker isOpen={isOpen} onClose={onClose} submitFile={submitFile} />
    </>
  );
}

export default App;
