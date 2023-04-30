import { useState, useEffect } from "react";
import axios from "axios";
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  Button,
  List,
  ListItem,
  ListIcon,
  useToast,
  Text,
} from "@chakra-ui/react";
import { BsFileFill, BsFolder } from "react-icons/bs";

const FilePicker = ({ isOpen, onClose, submitFile, backendAddress }) => {
  const toast = useToast();

  const [tree, setTree] = useState(null);
  const [file, setFile] = useState("");
  const getLocalFiles = async () => {
    try {
      const { data } = await axios.post(`http://${backendAddress}/picker`, {
        cmd: "ls",
      });
      setTree(data);
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

  const changeDirectory = async (dir) => {
    try {
      const { data } = await axios.post(`http://${backendAddress}/picker`, {
        cmd: "cd",
        dir,
      });
      setTree(data);
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

  useEffect(() => {
    getLocalFiles();
  }, []);

  return (
    <>
      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Choose a file</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <List spacing={2}>
              <ListItem onClick={() => changeDirectory("..")}>
                <ListIcon as={BsFolder} color="teal.500" />
                ..
              </ListItem>
              {tree !== null ? (
                tree.dirs.map((item, idx) => (
                  <ListItem
                    key={`dir-${idx}`}
                    onClick={() => changeDirectory(item)}
                  >
                    <ListIcon as={BsFolder} color="teal.500" />
                    {item}
                  </ListItem>
                ))
              ) : (
                <></>
              )}
              {tree !== null ? (
                tree.filenames.map((item, idx) => (
                  <ListItem key={`file-${idx}`} onClick={() => setFile(item)}>
                    <ListIcon as={BsFileFill} color="teal.500" />
                    {item}
                  </ListItem>
                ))
              ) : (
                <></>
              )}
            </List>
            <Text fontSize="xl">File selected: {file}</Text>
          </ModalBody>
          <ModalFooter>
            <Button colorScheme="red" mr={3} onClick={onClose}>
              Close
            </Button>
            <Button colorScheme="green" onClick={() => submitFile(file)}>
              Submit
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
};

export default FilePicker;
