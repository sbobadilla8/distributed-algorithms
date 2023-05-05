import { useEffect, useState } from "react";
import axios from "axios";
import {
  Button,
  Flex,
  Heading,
  IconButton,
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
import { BsXCircle } from "react-icons/bs";

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
        description: "Error sharing file",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const stopShare = async (file) => {
    try {
      const { data } = await axios.delete(
        `http://${backendAddress}/files?filename=${file.filename}&server=${serverAddress}`
      );
      setFiles(data);
    } catch (e) {
      toast({
        title: "Error",
        description: "Error dropping share.",
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
                <IconButton
                  aria-label="remove"
                  colorScheme="red"
                  size="sm"
                  onClick={() => stopShare(item)}
                  icon={<BsXCircle />}
                />
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
