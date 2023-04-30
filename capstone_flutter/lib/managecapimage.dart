/// This file is not in use for the final execution. This shows our experimentation on the technology

import 'package:amplify_api/amplify_api.dart';
import 'package:amplify_flutter/amplify_flutter.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import 'models/CapImage.dart';

class ManageCapImageScreen extends StatefulWidget {
  const ManageCapImageScreen({
    required this.capImage,
    super.key,
  });

  final CapImage? capImage;

  @override
  State<ManageCapImageScreen> createState() => _ManageCapImageScreenState();
}

class _ManageCapImageScreenState extends State<ManageCapImageScreen> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _titleController = TextEditingController();
  final TextEditingController _descriptionController = TextEditingController();
  final TextEditingController _pathController = TextEditingController();

  late final String _titleText;

  bool get _isCreate => _capImage == null;
  CapImage? get _capImage => widget.capImage;

  @override
  void initState() {
    super.initState();

    final capImage = _capImage;
    if (capImage != null) {
      _titleController.text = capImage.name;
      _descriptionController.text = capImage.description ?? '';
      _pathController.text = capImage.path ?? '';
      _titleText = 'Update image';
    } else {
      _titleText = 'Create image';
    }
  }

  @override
  void dispose() {
    _titleController.dispose();
    _descriptionController.dispose();
    _pathController.dispose();
    super.dispose();
  }

  Future<void> submitForm() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    // If the form is valid, submit the data
    final name = _titleController.text;
    final description = _descriptionController.text;
    final path = _pathController.text;

    if (_isCreate) {
      // Create a new budget entry
      final newEntry = CapImage(
        name: name,
        description: description.isNotEmpty ? description : null,
        path: path,
      );
      final request = ModelMutations.create(newEntry);
      final response = await Amplify.API.mutate(request: request).response;
      safePrint('Create result: $response');
    } else {
      // Update budgetEntry instead
      final updateCapImage = _capImage!.copyWith(
        name: name,
        description: description.isNotEmpty ? description : null,
        path: path,
      );
      final request = ModelMutations.update(updateCapImage);
      final response = await Amplify.API.mutate(request: request).response;
      safePrint('Update result: $response');
    }

    // Navigate back to homepage after create/update executes
    if (mounted) {
      context.pop();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_titleText),
      ),
      body: Align(
        alignment: Alignment.topCenter,
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 800),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: SingleChildScrollView(
              child: Form(
                key: _formKey,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    TextFormField(
                      controller: _titleController,
                      decoration: const InputDecoration(
                        labelText: 'Title (required)',
                      ),
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Please enter a image';
                        }
                        return null;
                      },
                    ),
                    TextFormField(
                      controller: _descriptionController,
                      decoration: const InputDecoration(
                        labelText: 'Description',
                      ),
                    ),
                    TextFormField(
                      controller: _pathController,
                      keyboardType: const TextInputType.numberWithOptions(
                        signed: false,
                        decimal: true,
                      ),
                      decoration: const InputDecoration(
                        labelText: 'Amount (required)',
                      ),
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Please enter an path';
                        }
                        final path = double.tryParse(value);
                        if (path == null || path <= 0) {
                          return 'Please enter a valid path';
                        }
                        return null;
                      },
                    ),
                    const SizedBox(height: 20),
                    ElevatedButton(
                      onPressed: submitForm,
                      child: Text(_titleText),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
