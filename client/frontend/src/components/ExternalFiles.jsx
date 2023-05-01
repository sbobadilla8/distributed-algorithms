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

const ExternalFiles = ({ serverAddress, backendAddress }) => {
  const toast = useToast();

  const [input, setInput] = useState("");
  const [results, setResults] = useState([]);

  const searchFile = async () => {
    try {
      const { data } = await axios.get(
        `http://${serverAddress}/file?input=${input}`
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

  const startDownload = async (item) => {
    try {
      const response = await axios.post(`http://${backendAddress}/download`, {
        filename: item.filename,
        size: item.size,
        clients: item.clients,
      });
      let flag = false;
      let intervalId = setInterval(async () => {
        const { data } = await axios.get(
          `http://${backendAddress}/download?filename=${item.filename}`
        );
        const progress = data.value;
        if (parseFloat(progress) < 1.0) {
          console.log(progress);
        } else {
          flag = true;
        }
      }, 1000);
      if (flag) {
        console.log(1);
        clearInterval(intervalId);
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
                    onClick={() => startDownload(item)}
                    icon={<BsDownload />}
                  />
                </StatGroup>
                <Progress value={80} />
              </Box>
            ))}
          </Stack>
        </CardBody>
      </Card>
    </>
  );
};

export default ExternalFiles;
