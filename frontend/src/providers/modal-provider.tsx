import {
  Dialog,
  DialogContent,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";

const ModalProvider = ({
  error,
  isOpen,
  onClose,
}: {
  error: string | null;
  isOpen: boolean;
  onClose: () => void;
}) => {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogTitle>Error</DialogTitle>
        <DialogDescription>{error}</DialogDescription>
      </DialogContent>
    </Dialog>
  );
};

export default ModalProvider;
