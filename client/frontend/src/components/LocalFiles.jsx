import { useEffect, useState } from "react";
import axios from "axios";
import {
  Button,
  Flex,
  Heading,
  Table,
  TableContainer,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
  useDisclosure,
  useToast,
} from "@chakra-ui/react";
import FilePicker from "./FilePicker.jsx";
import { humanFileSize } from "../utils/fileSize.js";

const LocalFiles = ({ backendAddress, serverAddress }) => {
  const toast = useToast();

  const [files, setFiles] = useState([]);
  const { isOpen, onOpen, onClose } = useDisclosure();

  const submitFile = async (file) => {
    try {
      const { data } = await axios.post(`http://${backendAddress}/files`, {
        file,
        serverAddress,
      });
      setFiles(data);
      onClose();
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

  const getFiles = async () => {
    try {
      const { data } = await axios.get(`http://${backendAddress}/files`);
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
      <Flex direction="row" justify="center">
        <Heading size="lg">Files being shared</Heading>
      </Flex>
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
                <Td>{humanFileSize(item.size)}</Td>
                <Td>{item.blocks}</Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      </TableContainer>
      <FilePicker
        isOpen={isOpen}
        onClose={onClose}
        submitFile={submitFile}
        backendAddress={backendAddress}
      />
    </>
  );
};

export default LocalFiles;
