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
  Stack,
  StackDivider,
  Stat,
  StatGroup,
  StatLabel,
  StatNumber,
  useToast,
} from "@chakra-ui/react";
import { BsDownload } from "react-icons/bs";

const ExternalFiles = ({ serverAddress }) => {
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
                    icon={<BsDownload />}
                  />
                </StatGroup>
              </Box>
            ))}
          </Stack>
        </CardBody>
      </Card>
    </>
  );
};

export default ExternalFiles;
