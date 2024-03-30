import SwiftUI
import CoreBluetooth

class BLEPeripheralDelegate: NSObject, CBPeripheralManagerDelegate {
    
    // Reference to the peripheral manager
    var peripheralManager: CBPeripheralManager!
    var characteristicString: CBMutableCharacteristic!
    var characteristicImage: CBMutableCharacteristic!
    var imageData = Data() // Buffer to store received image data
    
    // Reference to the ContentView for updating the UI
    var contentView: ContentView?
    
    // UUID for the BLE service and characteristic
    let serviceUUID = CBUUID(string: "0000ffe0-0000-1000-8000-00805f9b34fb")
    let characteristicStringUUID = CBUUID(string: "0000ffe1-0000-1000-8000-00805f9b34fb")
    let characteristicImageUUID = CBUUID(string: "0000ffe2-0000-1000-8000-00805f9b34fb")
    
    override init() {
        super.init()
        // Initialize the peripheral manager
        peripheralManager = CBPeripheralManager(delegate: self, queue: nil)
    }
    
    func peripheralManagerDidUpdateState(_ peripheral: CBPeripheralManager) {
        if peripheral.state == .poweredOn {
            // Bluetooth is powered on, start advertising the service
            startAdvertising()
        } else {
            // Handle other states as needed
        }
    }
    
    func startAdvertising() {
        // Create the characteristics
        characteristicString = CBMutableCharacteristic(type: characteristicStringUUID, properties: [.read, .write], value: nil, permissions: [.readable, .writeable])
        
        characteristicImage = CBMutableCharacteristic(type: characteristicImageUUID, properties: [.read, .write], value: nil, permissions: [.readable, .writeable])
        
        // Create the service
        let service = CBMutableService(type: serviceUUID, primary: true)
        service.characteristics = [characteristicString, characteristicImage]
        
        // Add the service to the peripheral manager
        peripheralManager.add(service)
        
        // Start advertising the service
        peripheralManager.startAdvertising([CBAdvertisementDataServiceUUIDsKey: [serviceUUID]])
    }
    
    func peripheralManager(_ peripheral: CBPeripheralManager, didAdd service: CBService, error: Error?) {
        if let error = error {
            print("Error adding service: \(error.localizedDescription)")
            return
        }
        print("Service added successfully")
    }
    
    func peripheralManagerDidStartAdvertising(_ peripheral: CBPeripheralManager, error: Error?) {
        if let error = error {
            print("Error starting advertising: \(error.localizedDescription)")
            return
        }
        print("Advertising started successfully")
    }
    
    func peripheralManager(_ peripheral: CBPeripheralManager, didReceiveRead request: CBATTRequest) {
        if request.characteristic.uuid == characteristicStringUUID {
            // Respond to read request with characteristic 1 value
            request.value = "Hello, Mac from Characteristic 1!".data(using: .utf8)
            peripheralManager.respond(to: request, withResult: .success)
        } else if request.characteristic.uuid == characteristicImageUUID {
            // Respond to read request with characteristic 2 value
            request.value = "Hello, Mac from Characteristic 2!".data(using: .utf8)
            peripheralManager.respond(to: request, withResult: .success)
        } else {
            // Handle other characteristics as needed
            peripheralManager.respond(to: request, withResult: .attributeNotFound)
        }
    }
    
    func peripheralManager(_ peripheral: CBPeripheralManager, didReceiveWrite requests: [CBATTRequest]) {
        for request in requests {
            if request.characteristic.uuid == characteristicStringUUID {
                // Handle write request with characteristic value
                if let value = request.value {
                    let receivedString = String(data: value, encoding: .utf8) ?? ""
                    print("Received message from Mac:", receivedString)
                    // Update the UI with the received message
                    contentView?.updateMessage(receivedString)
                }
                peripheralManager.respond(to: request, withResult: .success)
            } else if request.characteristic.uuid == characteristicImageUUID {
                if let value = request.value {
                    if let image = UIImage(data: value) { // For iOS
                        print("yay")
                        contentView?.updateImage(image)
                    }
                    else {
                        print("problem")
                    }
                }
            } else {
                // Handle other characteristics as needed
                peripheralManager.respond(to: request, withResult: .attributeNotFound)
            }
        }
    }
    
    // Function to reassemble the received image
    func reassembleImage() -> UIImage? {
        if let image = UIImage(data: imageData) {
            // Image successfully created
            return image
        } else {
            // Failed to create image
            print("Failed to create image from data")
            return nil
        }
    }
}

struct ImageView: View {
    var imageName: String
    
    var body: some View {
        Image(imageName)
            .resizable()
            .aspectRatio(contentMode: .fit)
            .frame(width: 256, height: 256)
            .clipped()
    }
}

struct ContentView: View {
    
    // Reference to the BLE peripheral delegate
    let blePeripheralDelegate = BLEPeripheralDelegate()
    
    // State variable to hold the received message
    @State private var receivedMessage: String = ""
    
    // State variable to hold the received image
    @State private var receivedImage: UIImage?
    
    var body: some View {
        VStack {
            Text("Neuromorphic Wildlife Camera")
                .font(.largeTitle)
                .padding()
            
            Text("Detection Status: \(receivedMessage)")
                .font(.title)
                .padding()
            
            Spacer()
            
            Image(systemName: "person")
                .resizable()
                .aspectRatio(contentMode: .fit)
                .frame(width: 300, height: 300)
                .padding()
        }
        .onAppear {
            // Set the ContentView reference in the BLEPeripheralDelegate
            blePeripheralDelegate.contentView = self
        }
    }
    
    // Function to update the received image
    func updateReceivedImage() {
        receivedImage = blePeripheralDelegate.reassembleImage()
    }
    
    // Function to update the received message
    func updateMessage(_ message: String) {
        receivedMessage = message
    }
    
    // Function to update the received image
    func updateImage(_ image: UIImage) {
        receivedImage = image
    }
}
